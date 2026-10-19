"""
Data collection module for SignBridge.
Manages structured CSV storage of labeled hand landmark samples with session
metadata, class balance tracking, and dataset validation.
"""

import os
import sys
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
import pandas as pd


try:
    from backend.preprocessing import TOTAL_FEATURES, get_feature_names
except ImportError:
    from src.preprocessing import TOTAL_FEATURES, get_feature_names

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DEFAULT_DATASET_FILE = os.path.join(DEFAULT_DATA_DIR, "isl_dataset.csv")

METADATA_COLUMNS = ["sample_id", "label", "session_id", "participant_id", "handedness", "timestamp"]

CORE_ISL_GESTURES = ["HELLO", "HELP", "NO", "THANK_YOU", "YES"]
ISL_ALPHABET_LETTERS = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
ALL_TARGET_CLASSES = ISL_ALPHABET_LETTERS + CORE_ISL_GESTURES


def get_dataset_columns() -> List[str]:
    """Returns the ordered list of all CSV columns."""
    return METADATA_COLUMNS + get_feature_names()



class DatasetManager:
    """Manages reading, appending, validating, and summarizing the sign dataset."""

    def __init__(self, dataset_path: Optional[str] = None):
        self.dataset_path = dataset_path or DEFAULT_DATASET_FILE
        self._ensure_dataset_initialized()

    def _ensure_dataset_initialized(self) -> None:
        """Create directory and CSV with headers if it does not exist."""
        os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)
        if not os.path.exists(self.dataset_path) or os.path.getsize(self.dataset_path) == 0:
            df = pd.DataFrame(columns=get_dataset_columns())
            df.to_csv(self.dataset_path, index=False)

    def append_sample(
        self,
        label: str,
        features: np.ndarray,
        session_id: str,
        participant_id: str = "user_1",
        handedness: str = "Right",
    ) -> bool:
        """
        Append a single feature vector (63 floats) to the dataset CSV.
        """
        if features is None or len(features) != TOTAL_FEATURES:
            raise ValueError(f"Features must have exactly {TOTAL_FEATURES} values.")

        clean_label = str(label).strip().upper()
        if not clean_label:
            raise ValueError("Sign label cannot be empty.")

        sample_id = str(uuid.uuid4())[:8]
        timestamp = datetime.utcnow().isoformat()

        row_dict = {
            "sample_id": sample_id,
            "label": clean_label,
            "session_id": session_id,
            "participant_id": participant_id,
            "handedness": handedness,
            "timestamp": timestamp,
        }

        feature_names = get_feature_names()
        for idx, feat_name in enumerate(feature_names):
            row_dict[feat_name] = float(features[idx])

        row_df = pd.DataFrame([row_dict], columns=get_dataset_columns())
        row_df.to_csv(self.dataset_path, mode="a", header=False, index=False)
        return True

    def append_samples_batch(
        self,
        samples: List[Tuple[str, np.ndarray, str, str, str]],
    ) -> int:
        """
        Batch append multiple samples.
        Each item: (label, features, session_id, participant_id, handedness)
        """
        if not samples:
            return 0

        rows = []
        feature_names = get_feature_names()
        for label, feats, sess_id, part_id, hand in samples:
            clean_label = str(label).strip().upper()
            row = {
                "sample_id": str(uuid.uuid4())[:8],
                "label": clean_label,
                "session_id": sess_id,
                "participant_id": part_id,
                "handedness": hand,
                "timestamp": datetime.utcnow().isoformat(),
            }
            for idx, feat_name in enumerate(feature_names):
                row[feat_name] = float(feats[idx])
            rows.append(row)

        df = pd.DataFrame(rows, columns=get_dataset_columns())
        df.to_csv(self.dataset_path, mode="a", header=False, index=False)
        return len(rows)

    def load_dataset(self) -> pd.DataFrame:
        """Load current dataset as a Pandas DataFrame."""
        if not os.path.exists(self.dataset_path) or os.path.getsize(self.dataset_path) == 0:
            return pd.DataFrame(columns=get_dataset_columns())
        return pd.read_csv(self.dataset_path)

    def get_class_counts(self) -> Dict[str, int]:
        """Return sample counts grouped by sign label."""
        df = self.load_dataset()
        if df.empty or "label" not in df.columns:
            return {}
        counts = df["label"].value_counts().to_dict()
        return {str(k): int(v) for k, v in counts.items()}

    def validate_dataset(self, min_samples_per_class: int = 15) -> Tuple[bool, List[str]]:
        """
        Validate dataset integrity:
        1. Checks for required columns.
        2. Detects null / NaN values in features.
        3. Checks sample counts per class.
        4. Detects potential class imbalance.
        """
        issues = []
        df = self.load_dataset()

        if df.empty:
            issues.append("Dataset is empty. No samples have been recorded yet.")
            return False, issues

        missing_cols = [c for c in get_dataset_columns() if c not in df.columns]
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols[:5]}...")
            return False, issues

        feature_cols = get_feature_names()
        nan_counts = df[feature_cols].isna().sum().sum()
        if nan_counts > 0:
            issues.append(f"Found {nan_counts} missing or NaN values across feature columns.")

        class_counts = self.get_class_counts()
        if len(class_counts) < 2:
            issues.append(f"Dataset has only {len(class_counts)} class. At least 2 distinct classes are required for classification.")

        for cls, count in class_counts.items():
            if count < min_samples_per_class:
                issues.append(
                    f"Class '{cls}' has only {count} samples. Recommended minimum is {min_samples_per_class}."
                )

        # Check severe imbalance (> 5:1 ratio between largest and smallest class)
        if class_counts:
            min_c = min(class_counts.values())
            max_c = max(class_counts.values())
            if min_c > 0 and (max_c / min_c) > 5.0:
                issues.append(
                    f"Significant class imbalance detected (Max: {max_c}, Min: {min_c}). "
                    "Consider capturing more samples for underrepresented signs."
                )

        is_valid = len(issues) == 0
        return is_valid, issues

    def delete_samples_for_label(self, label: str) -> int:
        """
        Delete all samples associated with a specific label.
        Returns the number of rows removed.
        """
        df = self.load_dataset()
        if df.empty or "label" not in df.columns:
            return 0
        clean_label = str(label).strip().upper()
        initial_count = len(df)
        remaining_df = df[df["label"].str.strip().str.upper() != clean_label]
        removed_count = initial_count - len(remaining_df)
        if removed_count > 0:
            remaining_df.to_csv(self.dataset_path, index=False)
        return removed_count

    def clear_dataset(self) -> None:
        """Reset dataset to empty schema."""
        df = pd.DataFrame(columns=get_dataset_columns())
        df.to_csv(self.dataset_path, index=False)

    def get_alphabet_coverage_status(self, trained_classes: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Calculates accurate coverage status for all 26 manual alphabet letters (A-Z).
        Statuses:
          - 'Active in classifier': trained model includes this letter.
          - 'Ready to train': usable samples exist in dataset, awaiting model training.
          - 'Needs data': 0 samples collected so far.
        """
        counts = self.get_class_counts()
        trained_set = set(str(c).upper() for c in (trained_classes or []))
        
        status_list = []
        for letter in ISL_ALPHABET_LETTERS:
            count = counts.get(letter, 0)
            if letter in trained_set:
                status = "Active in classifier"
                status_code = "ACTIVE"
            elif count > 0:
                status = "Ready to train"
                status_code = "READY"
            else:
                status = "Needs data"
                status_code = "NEEDS_DATA"

            status_list.append({
                "letter": letter,
                "count": count,
                "status": status,
                "status_code": status_code,
            })
        return status_list


# Biomechanical & linguistic guide for Indian Sign Language (ISL) single-hand fingerspelling
ISL_ALPHABET_GUIDE: Dict[str, Dict[str, str]] = {
    "A": {
        "posture": "Closed fist with thumb upright alongside the index finger.",
        "tips": "Keep wrist straight and face thumb toward the camera.",
        "motion": "Static hand posture.",
    },
    "B": {
        "posture": "Flat open palm facing forward, four fingers straight up, thumb tucked across palm.",
        "tips": "Keep fingers closely joined and vertical.",
        "motion": "Static hand posture.",
    },
    "C": {
        "posture": "Arched hand forming a clear 'C' curve between fingers and thumb.",
        "tips": "Show the lateral profile of the C to camera for clearest landmark capture.",
        "motion": "Static hand posture.",
    },
    "D": {
        "posture": "Index finger extended straight up; thumb and other three fingers curved to form an enclosed loop.",
        "tips": "Keep index finger perfectly vertical.",
        "motion": "Static hand posture.",
    },
    "E": {
        "posture": "All four fingers curled tightly downwards with tips resting against the tucked thumb.",
        "tips": "Fingernails should face forward.",
        "motion": "Static hand posture.",
    },
    "F": {
        "posture": "Index finger and thumb touching at tips in an 'OK' circle; middle, ring, and pinky extended upward.",
        "tips": "Keep the three extended fingers spread cleanly.",
        "motion": "Static hand posture.",
    },
    "G": {
        "posture": "Index finger and thumb parallel pointing horizontally; other fingers curled into palm.",
        "tips": "Point index finger horizontally across the frame.",
        "motion": "Static hand posture.",
    },
    "H": {
        "posture": "Index and middle fingers extended together pointing horizontally; thumb and other fingers curled.",
        "tips": "Keep index and middle fingers joined and parallel.",
        "motion": "Static hand posture.",
    },
    "I": {
        "posture": "Pinky finger extended straight up; index, middle, ring, and thumb curled into a fist.",
        "tips": "Keep pinky vertical and palm facing forward.",
        "motion": "Static hand posture.",
    },
    "J": {
        "posture": "Pinky extended upright in 'I' shape (the key inflection posture).",
        "tips": "Hold pinky upright steadily for static landmark recognition.",
        "motion": "Note: Standard fingerspelling draws a J curve in air; hold the static starting/inflection handshape.",
    },
    "K": {
        "posture": "Index finger pointing up, middle finger angled forward/down, thumb placed at the base.",
        "tips": "Fingers form a 'K' shape from the camera's perspective.",
        "motion": "Static hand posture.",
    },
    "L": {
        "posture": "Thumb and index finger extended at a 90-degree right angle forming an 'L'; others curled.",
        "tips": "Clear right-angle separation between thumb and index.",
        "motion": "Static hand posture.",
    },
    "M": {
        "posture": "Thumb tucked underneath the first three folded fingers (index, middle, ring); pinky curled alongside.",
        "tips": "Three folded knuckles visible above the thumb.",
        "motion": "Static hand posture.",
    },
    "N": {
        "posture": "Thumb tucked underneath the first two folded fingers (index, middle).",
        "tips": "Two folded knuckles visible above the thumb.",
        "motion": "Static hand posture.",
    },
    "O": {
        "posture": "All fingertips curved forward to touch the thumb tip, forming a circular 'O'.",
        "tips": "Show clear circular opening to the camera.",
        "motion": "Static hand posture.",
    },
    "P": {
        "posture": "Index finger pointing forward/down, middle finger pointing down, thumb resting between.",
        "tips": "Downward angled variation of the K posture.",
        "motion": "Static hand posture.",
    },
    "Q": {
        "posture": "Index finger and thumb pointing downwards in a loose pinch.",
        "tips": "Downward angled variation of the G posture.",
        "motion": "Static hand posture.",
    },
    "R": {
        "posture": "Index and middle fingers crossed/intertwined and extended straight up; other fingers curled.",
        "tips": "Middle finger wraps closely across the index finger.",
        "motion": "Static hand posture.",
    },
    "S": {
        "posture": "Tight fist with thumb wrapped across the front of the curled fingers.",
        "tips": "Distinct from 'A' where thumb rests alongside the index.",
        "motion": "Static hand posture.",
    },
    "T": {
        "posture": "Thumb tucked between the curled index finger and middle finger.",
        "tips": "Thumb tip pokes out slightly between index and middle knuckles.",
        "motion": "Static hand posture.",
    },
    "U": {
        "posture": "Index and middle fingers extended straight up together; ring, pinky, and thumb curled.",
        "tips": "Keep the two fingers touching (no gap).",
        "motion": "Static hand posture.",
    },
    "V": {
        "posture": "Index and middle fingers extended in a spread 'V' shape (peace sign); other fingers curled.",
        "tips": "Clear spread gap between index and middle fingers.",
        "motion": "Static hand posture.",
    },
    "W": {
        "posture": "Index, middle, and ring fingers extended upward in a 'W'; pinky and thumb tucked.",
        "tips": "Three extended fingers spread evenly.",
        "motion": "Static hand posture.",
    },
    "X": {
        "posture": "Index finger bent like a hook; other fingers curled into a fist.",
        "tips": "Crooked index finger clearly visible.",
        "motion": "Static hand posture.",
    },
    "Y": {
        "posture": "Thumb and pinky finger extended outward (shaka shape); middle three fingers curled.",
        "tips": "Hold palm facing camera with thumb and pinky wide.",
        "motion": "Static hand posture.",
    },
    "Z": {
        "posture": "Index finger extended pointing forward (the key pointing posture).",
        "tips": "Hold index finger forward steadily for static landmark recognition.",
        "motion": "Note: Standard fingerspelling traces a Z path; hold the static index posture.",
    },
}

