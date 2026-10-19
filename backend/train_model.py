"""
Model training pipeline for SignBridge.
Loads labeled landmark features, applies group-aware / stratified splitting to prevent
leakage across recording sessions, trains a Random Forest Classifier, computes
comprehensive evaluation metrics, plots a confusion matrix, and saves the artifact via joblib.
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GroupShuffleSplit, StratifiedShuffleSplit

try:
    from backend.data_collection import DatasetManager
    from backend.preprocessing import TOTAL_FEATURES, get_feature_names
except ImportError:
    from src.data_collection import DatasetManager
    from src.preprocessing import TOTAL_FEATURES, get_feature_names

DEFAULT_MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
DEFAULT_MODEL_FILE = os.path.join(DEFAULT_MODEL_DIR, "isl_classifier.joblib")


class ModelTrainer:
    """Manages dataset loading, model training, cross-validation, and metric reporting."""

    def __init__(
        self,
        dataset_path: Optional[str] = None,
        model_save_path: Optional[str] = None,
        n_estimators: int = 150,
        random_state: int = 42,
    ):
        self.dataset_manager = DatasetManager(dataset_path)
        self.model_save_path = model_save_path or DEFAULT_MODEL_FILE
        self.n_estimators = n_estimators
        self.random_state = random_state

    def prepare_data(
        self,
        test_size: float = 0.2,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str], str]:
        """
        Extract features, targets, and group identifiers.
        Splits data cleanly without session-level leakage if session_id is available.
        """
        df = self.dataset_manager.load_dataset()
        if df.empty:
            raise ValueError("Dataset is empty. Cannot train model.")

        feature_cols = get_feature_names()
        for col in feature_cols:
            if col not in df.columns:
                raise ValueError(f"Required feature column '{col}' missing from dataset.")

        # Drop any row with missing labels or NaN features
        clean_df = df.dropna(subset=["label"] + feature_cols).copy()
        if len(clean_df) < 10:
            raise ValueError(f"Insufficient samples for training ({len(clean_df)} found, at least 10 required).")

        labels = clean_df["label"].astype(str).str.strip().str.upper().values
        unique_classes = sorted(list(set(labels)))
        if len(unique_classes) < 2:
            raise ValueError(f"Need at least 2 distinct classes to train a classifier. Found: {unique_classes}")

        X = clean_df[feature_cols].to_numpy(dtype=np.float32)
        y = labels

        # Determine split strategy: Group-based vs Stratified vs Random
        split_strategy = "stratified"
        try:
            if "session_id" in clean_df.columns:
                session_groups = clean_df["session_id"].astype(str).values
                unique_sessions_per_class = clean_df.groupby("label")["session_id"].nunique()
                # If every class has multiple recording sessions, use GroupShuffleSplit to prevent session leakage
                if (unique_sessions_per_class >= 2).all() and len(np.unique(session_groups)) >= 4:
                    gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=self.random_state)
                    train_idx, test_idx = next(gss.split(X, y, groups=session_groups))
                    split_strategy = "group_session_split"
                else:
                    sss = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=self.random_state)
                    train_idx, test_idx = next(sss.split(X, y))
                    split_strategy = "stratified"
            else:
                sss = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=self.random_state)
                train_idx, test_idx = next(sss.split(X, y))
                split_strategy = "stratified"
        except Exception:
            # Safe fallback to random split if any class has too few samples for stratified splitting
            from sklearn.model_selection import train_test_split
            train_idx, test_idx = train_test_split(
                np.arange(len(X)), test_size=test_size, random_state=self.random_state, shuffle=True
            )
            split_strategy = "random_shuffle_split"

        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        return X_train, X_test, y_train, y_test, unique_classes, split_strategy

    def train_and_evaluate(
        self,
        test_size: float = 0.2,
    ) -> Dict[str, Any]:
        """
        Train Random Forest classifier, evaluate on test set, and save model artifact.
        """
        X_train, X_test, y_train, y_test, classes, split_used = self.prepare_data(test_size=test_size)

        clf = RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=16,
            min_samples_split=2,
            min_samples_leaf=1,
            class_weight="balanced",
            random_state=self.random_state,
            n_jobs=1,
        )

        clf.fit(X_train, y_train)


        y_pred = clf.predict(X_test)

        acc = float(accuracy_score(y_test, y_pred))
        precision_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
        precision_weighted = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
        recall_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
        recall_weighted = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
        f1_macro = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
        f1_weighted = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

        cm = confusion_matrix(y_test, y_pred, labels=classes)
        clf_report = classification_report(y_test, y_pred, labels=classes, output_dict=True, zero_division=0)

        # Feature importances
        feature_names = get_feature_names()
        importances = clf.feature_importances_
        top_feat_indices = np.argsort(importances)[::-1][:10]
        top_features = [(feature_names[i], float(importances[i])) for i in top_feat_indices]

        # Save package artifact with metadata
        model_artifact = {
            "model": clf,
            "classes": classes,
            "feature_names": feature_names,
            "metrics": {
                "accuracy": acc,
                "precision_macro": precision_macro,
                "precision_weighted": precision_weighted,
                "recall_macro": recall_macro,
                "recall_weighted": recall_weighted,
                "f1_macro": f1_macro,
                "f1_weighted": f1_weighted,
            },
            "training_samples": len(X_train),
            "testing_samples": len(X_test),
            "split_strategy": split_used,
            "trained_at": datetime.utcnow().isoformat(),
            "n_estimators": self.n_estimators,
        }

        os.makedirs(os.path.dirname(self.model_save_path), exist_ok=True)
        joblib.dump(model_artifact, self.model_save_path)

        return {
            "model_path": self.model_save_path,
            "classes": classes,
            "accuracy": acc,
            "precision_macro": precision_macro,
            "precision_weighted": precision_weighted,
            "recall_macro": recall_macro,
            "recall_weighted": recall_weighted,
            "f1_macro": f1_macro,
            "f1_weighted": f1_weighted,
            "confusion_matrix": cm,
            "classification_report": clf_report,
            "top_features": top_features,
            "train_size": len(X_train),
            "test_size": len(X_test),
            "split_strategy": split_used,
        }

    def render_confusion_matrix_plot(
        self,
        cm: np.ndarray,
        classes: List[str],
        title: str = "SignBridge Gesture Recognition Confusion Matrix",
    ) -> plt.Figure:
        """Create a clean, publication-ready seaborn heatmap of the confusion matrix."""
        fig, ax = plt.subplots(figsize=(max(6, len(classes) * 1.1), max(5, len(classes) * 0.9)))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=classes,
            yticklabels=classes,
            cbar=False,
            ax=ax,
            linewidths=1.0,
            linecolor="#e0e0e0",
        )
        ax.set_title(title, fontsize=12, pad=12, weight="bold")
        ax.set_xlabel("Predicted Sign", fontsize=10, weight="bold")
        ax.set_ylabel("True Ground Truth Sign", fontsize=10, weight="bold")
        plt.tight_layout()
        return fig


if __name__ == "__main__":
    print("[SignBridge] Initializing training pipeline...")
    trainer = ModelTrainer()
    results = trainer.train_and_evaluate(test_size=0.2)
    print("\n--- Training Results ---")
    print(f"Model saved to: {results['model_path']}")
    print(f"Classes: {results['classes']}")
    print(f"Split Strategy Used: {results['split_strategy']}")
    print(f"Training Samples: {results['train_size']}, Testing Samples: {results['test_size']}")
    print(f"Accuracy: {results['accuracy']:.4f}")
    print(f"Precision (Macro): {results['precision_macro']:.4f}")
    print(f"Recall (Macro): {results['recall_macro']:.4f}")
    print(f"F1 Score (Macro): {results['f1_macro']:.4f}")
    print(f"F1 Score (Weighted): {results['f1_weighted']:.4f}")
    print("\nConfusion Matrix:")
    print(results['confusion_matrix'])

