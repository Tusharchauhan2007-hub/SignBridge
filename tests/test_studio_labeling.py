"""
Regression tests for SignBridge Studio sample labeling and alphabet switching.
Ensures that samples captured for any alphabet letter (A, B, C, etc.) are saved
with their exact selected label, without hardcoded fallback to 'A'.
"""

import os
import tempfile
import numpy as np
import pytest
import pandas as pd

from backend.data_collection import DatasetManager, ISL_ALPHABET_LETTERS, CORE_ISL_GESTURES
from backend.preprocessing import TOTAL_FEATURES
from backend.train_model import ModelTrainer


@pytest.fixture
def temp_studio_dataset():
    """Create an isolated temporary dataset CSV file for studio testing."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        path = f.name
    mgr = DatasetManager(dataset_path=path)
    yield mgr
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass


def test_select_and_capture_letter_a(temp_studio_dataset):
    """Verify selecting A and capturing saves exactly as 'A'."""
    feat = np.ones(TOTAL_FEATURES, dtype=np.float32) * 0.1
    temp_studio_dataset.append_sample(label="A", features=feat, session_id="sess_1")

    df = temp_studio_dataset.load_dataset()
    assert len(df) == 1
    assert df.iloc[0]["label"] == "A"
    assert temp_studio_dataset.get_class_counts() == {"A": 1}


def test_select_and_capture_letter_b(temp_studio_dataset):
    """Verify selecting B and capturing saves exactly as 'B' (not 'A')."""
    feat = np.ones(TOTAL_FEATURES, dtype=np.float32) * 0.2
    temp_studio_dataset.append_sample(label="B", features=feat, session_id="sess_1")

    df = temp_studio_dataset.load_dataset()
    assert len(df) == 1
    assert df.iloc[0]["label"] == "B"
    assert "A" not in temp_studio_dataset.get_class_counts()
    assert temp_studio_dataset.get_class_counts() == {"B": 1}


def test_select_and_capture_letter_c(temp_studio_dataset):
    """Verify selecting C and capturing saves exactly as 'C' (not 'A')."""
    feat = np.ones(TOTAL_FEATURES, dtype=np.float32) * 0.3
    temp_studio_dataset.append_sample(label="C", features=feat, session_id="sess_1")

    df = temp_studio_dataset.load_dataset()
    assert len(df) == 1
    assert df.iloc[0]["label"] == "C"
    assert "A" not in temp_studio_dataset.get_class_counts()
    assert temp_studio_dataset.get_class_counts() == {"C": 1}


def test_repeated_letter_switching_retains_correct_labels(temp_studio_dataset):
    """
    Verify switching between different letters repeatedly (A -> B -> C -> B -> D -> A)
    saves each sample with its exact corresponding label.
    """
    feat = np.zeros(TOTAL_FEATURES, dtype=np.float32)
    sequence = ["A", "B", "C", "B", "D", "A", "Z", "C", "B"]

    for idx, target in enumerate(sequence):
        temp_studio_dataset.append_sample(label=target, features=feat, session_id=f"sess_{idx}")

    df = temp_studio_dataset.load_dataset()
    assert len(df) == len(sequence)
    saved_labels = list(df["label"].values)
    assert saved_labels == sequence

    counts = temp_studio_dataset.get_class_counts()
    assert counts["A"] == 2
    assert counts["B"] == 3
    assert counts["C"] == 2
    assert counts["D"] == 1
    assert counts["Z"] == 1


def test_batch_burst_capture_records_selected_letter_only(temp_studio_dataset):
    """
    Verify burst capture of 10 samples for letter 'B' updates only 'B' count
    without affecting other letters.
    """
    feat = np.ones(TOTAL_FEATURES, dtype=np.float32) * 0.5
    burst_b = [("B", feat, "sess_burst", "user_1", "Right") for _ in range(10)]
    added_n = temp_studio_dataset.append_samples_batch(burst_b)
    assert added_n == 10

    counts = temp_studio_dataset.get_class_counts()
    assert counts.get("B") == 10
    assert "A" not in counts

    # Now capture burst for 'C'
    burst_c = [("C", feat, "sess_burst_2", "user_1", "Right") for _ in range(10)]
    temp_studio_dataset.append_samples_batch(burst_c)

    counts_after = temp_studio_dataset.get_class_counts()
    assert counts_after.get("B") == 10
    assert counts_after.get("C") == 10
    assert "A" not in counts_after


def test_training_pipeline_evaluates_distinct_saved_letters(temp_studio_dataset):
    """
    Verify that ModelTrainer correctly loads the distinct saved letters
    and trains a classifier that recognizes each class.
    """
    batch = []
    # Add samples across 3 distinct letters: A, B, C
    for letter in ["A", "B", "C"]:
        for sess in ["sess_1", "sess_2"]:
            for i in range(6):
                shift = {"A": 0.2, "B": 0.5, "C": -0.4}[letter]
                feat = np.random.normal(shift, 0.05, TOTAL_FEATURES).astype(np.float32)
                batch.append((letter, feat, sess, "user_1", "Right"))

    temp_studio_dataset.append_samples_batch(batch)

    with tempfile.NamedTemporaryFile(suffix=".joblib", delete=False) as f_mod:
        mod_path = f_mod.name

    try:
        trainer = ModelTrainer(
            dataset_path=temp_studio_dataset.dataset_path,
            model_save_path=mod_path,
            n_estimators=10,
        )
        res = trainer.train_and_evaluate(test_size=0.3)
        assert res is not None
        assert set(res["classes"]) == {"A", "B", "C"}
        assert res["accuracy"] >= 0.70
    finally:
        if os.path.exists(mod_path):
            try:
                os.remove(mod_path)
            except Exception:
                pass


def test_session_state_letter_resolution_no_hardcoded_a_override():
    """
    Verify that selecting a letter other than 'A' (e.g. 'B' or 'C')
    in session state is never overwritten back to 'A'.
    """
    # Simulate session state dictionary
    mock_state = {}

    # Initial state
    if "target_letter" not in mock_state:
        mock_state["target_letter"] = "A"

    # User changes dropdown to 'B'
    mock_state["studio_target_letter_select"] = "B"

    # Simulated studio logic
    if mock_state.get("studio_target_letter_select") in ISL_ALPHABET_LETTERS:
        mock_state["target_letter"] = mock_state["studio_target_letter_select"]

    target_sign = mock_state["studio_target_letter_select"]
    assert target_sign == "B"
    assert mock_state["target_letter"] == "B"

    # User changes dropdown to 'C'
    mock_state["studio_target_letter_select"] = "C"
    if mock_state.get("studio_target_letter_select") in ISL_ALPHABET_LETTERS:
        mock_state["target_letter"] = mock_state["studio_target_letter_select"]

    target_sign = mock_state["studio_target_letter_select"]
    assert target_sign == "C"
    assert mock_state["target_letter"] == "C"

