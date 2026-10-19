"""
Unit tests for ModelTrainer pipeline, evaluation metrics, and model artifact loading.
"""

import os
import tempfile
import numpy as np
import pytest

from src.data_collection import DatasetManager
from src.predictor import SignPredictor
from src.preprocessing import TOTAL_FEATURES
from src.train_model import ModelTrainer


@pytest.fixture
def temp_ml_workspace():
    """Create a temporary dataset and model file for end-to-end training test."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f_csv:
        csv_path = f_csv.name
    with tempfile.NamedTemporaryFile(suffix=".joblib", delete=False) as f_model:
        model_path = f_model.name

    dm = DatasetManager(dataset_path=csv_path)

    # Populate with minimal valid samples across 2 classes
    batch = []
    for cls_name in ["HELLO", "YES"]:
        for sess_id in ["s1", "s2"]:
            for i in range(8):
                feat = np.random.normal(0.5 if cls_name == "HELLO" else -0.5, 0.05, TOTAL_FEATURES).astype(np.float32)
                batch.append((cls_name, feat, sess_id, f"user_{i%2}", "Right"))

    dm.append_samples_batch(batch)

    yield csv_path, model_path

    for p in [csv_path, model_path]:
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass


def test_model_trainer_pipeline(temp_ml_workspace):
    csv_path, model_path = temp_ml_workspace
    trainer = ModelTrainer(dataset_path=csv_path, model_save_path=model_path, n_estimators=10)

    # Train and evaluate
    res = trainer.train_and_evaluate(test_size=0.25)
    assert res is not None
    assert "accuracy" in res
    assert 0.0 <= res["accuracy"] <= 1.0
    assert len(res["classes"]) == 2
    assert os.path.exists(model_path)

    # Verify model artifact can be loaded by SignPredictor
    p = SignPredictor(model_path=model_path)
    assert p.is_loaded
    assert set(p.classes) == {"HELLO", "YES"}

    # Test confusion matrix plot creation
    fig = trainer.render_confusion_matrix_plot(res["confusion_matrix"], res["classes"])
    assert fig is not None


def test_model_trainer_insufficient_classes(temp_ml_workspace):
    csv_path, model_path = temp_ml_workspace
    dm = DatasetManager(dataset_path=csv_path)
    dm.clear_dataset()
    # Add only 1 class
    for i in range(12):
        dm.append_sample("ONLY_ONE", np.zeros(TOTAL_FEATURES, dtype=np.float32), "s1")

    trainer = ModelTrainer(dataset_path=csv_path, model_save_path=model_path)
    with pytest.raises(ValueError):
        trainer.train_and_evaluate()

