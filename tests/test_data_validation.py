"""
Unit tests for dataset collection, CSV schema validation, and balance checks.
"""

import os
import tempfile
import numpy as np
import pytest

from src.data_collection import DatasetManager, get_dataset_columns
from src.preprocessing import TOTAL_FEATURES


@pytest.fixture
def temp_dataset():
    """Create a temporary dataset CSV file."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        path = f.name
    mgr = DatasetManager(dataset_path=path)
    yield mgr
    if os.path.exists(path):
        os.remove(path)


def test_dataset_initialization(temp_dataset):
    df = temp_dataset.load_dataset()
    expected_cols = get_dataset_columns()
    assert list(df.columns) == expected_cols
    assert df.empty


def test_append_sample(temp_dataset):
    sample_feat = np.ones(TOTAL_FEATURES, dtype=np.float32) * 0.5
    success = temp_dataset.append_sample(
        label="HELLO",
        features=sample_feat,
        session_id="sess_test",
        participant_id="user_test",
        handedness="Right",
    )
    assert success
    df = temp_dataset.load_dataset()
    assert len(df) == 1
    assert df.iloc[0]["label"] == "HELLO"
    assert df.iloc[0]["session_id"] == "sess_test"
    assert pytest.approx(df.iloc[0]["lm_0_x"], abs=1e-5) == 0.5


def test_invalid_append(temp_dataset):
    # Invalid feature count
    with pytest.raises(ValueError):
        temp_dataset.append_sample("HELLO", np.zeros(20), "s1")

    # Empty label
    with pytest.raises(ValueError):
        temp_dataset.append_sample("", np.zeros(TOTAL_FEATURES), "s1")


def test_class_counts_and_validation(temp_dataset):
    feat = np.zeros(TOTAL_FEATURES, dtype=np.float32)

    # Empty dataset validation
    is_valid, issues = temp_dataset.validate_dataset()
    assert not is_valid
    assert any("empty" in msg.lower() for msg in issues)

    # Add samples for only 1 class
    for _ in range(5):
        temp_dataset.append_sample("HELLO", feat, "s1")

    counts = temp_dataset.get_class_counts()
    assert counts.get("HELLO") == 5

    # Should fail validation because only 1 class and < 15 samples
    is_valid, issues = temp_dataset.validate_dataset(min_samples_per_class=10)
    assert not is_valid
    assert any("at least 2 distinct classes" in msg.lower() for msg in issues)


def test_delete_samples_for_label(temp_dataset):
    feat = np.zeros(TOTAL_FEATURES, dtype=np.float32)
    temp_dataset.append_sample("A", feat, "s1")
    temp_dataset.append_sample("A", feat, "s1")
    temp_dataset.append_sample("B", feat, "s1")

    assert temp_dataset.get_class_counts()["A"] == 2
    assert temp_dataset.get_class_counts()["B"] == 1

    deleted_count = temp_dataset.delete_samples_for_label("A")
    assert deleted_count == 2
    assert "A" not in temp_dataset.get_class_counts()
    assert temp_dataset.get_class_counts()["B"] == 1


def test_alphabet_coverage_status(temp_dataset):
    feat = np.zeros(TOTAL_FEATURES, dtype=np.float32)
    # Collect sample for B
    temp_dataset.append_sample("B", feat, "s1")

    # Suppose model is trained on ['A']
    coverage = temp_dataset.get_alphabet_coverage_status(trained_classes=["A"])
    cov_dict = {item["letter"]: item for item in coverage}

    # A has 0 samples in CSV, but is trained in model -> 'Active in classifier'
    assert cov_dict["A"]["status"] == "Active in classifier"
    assert cov_dict["A"]["status_code"] == "ACTIVE"

    # B has 1 sample in CSV, not in trained model -> 'Ready to train'
    assert cov_dict["B"]["status"] == "Ready to train"
    assert cov_dict["B"]["status_code"] == "READY"
    assert cov_dict["B"]["count"] == 1

    # C has 0 samples in CSV, not in trained model -> 'Needs data'
    assert cov_dict["C"]["status"] == "Needs data"
    assert cov_dict["C"]["status_code"] == "NEEDS_DATA"
    assert cov_dict["C"]["count"] == 0

