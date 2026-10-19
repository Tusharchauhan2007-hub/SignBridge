"""
Unit tests for strict free-only policy and hard resource budget enforcement.
"""

import os
import tempfile
import pytest

from config import (
    MAX_DATASETS,
    MAX_EXTRACTED_STORAGE_BYTES,
    MAX_KAGGLE_API_REQUESTS,
    MAX_TOTAL_DOWNLOAD_BYTES,
    MAX_TRAINING_IMAGES,
    ResourceBudgetTracker,
)
from prepare_dataset import is_safe_zip_path


@pytest.fixture
def temp_tracker():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name
    tracker = ResourceBudgetTracker(usage_path=path)
    yield tracker
    if os.path.exists(path):
        os.remove(path)


def test_download_budget_enforcement(temp_tracker):
    # Test valid download within budget
    valid_size = 100 * 1024 * 1024  # 100 MB
    allowed, msg = temp_tracker.check_can_download(valid_size)
    assert allowed
    temp_tracker.record_download("ds_1", valid_size)

    # Test rejection of excessive download (> 2 GB)
    too_big = (MAX_TOTAL_DOWNLOAD_BYTES) + 1024
    allowed, msg = temp_tracker.check_can_download(too_big)
    assert not allowed
    assert "exceeds remaining budget" in msg.lower()

    # Test rejection of unknown/none size
    allowed, msg = temp_tracker.check_can_download(None)
    assert not allowed
    assert "unknown" in msg.lower()


def test_extracted_storage_enforcement(temp_tracker):
    # Within 5 GB limit
    valid_extract = 200 * 1024 * 1024  # 200 MB
    allowed, msg = temp_tracker.check_can_extract(valid_extract)
    assert allowed
    temp_tracker.record_extraction("ds_1", valid_extract)

    # Exceeding 5 GB limit
    too_large = MAX_EXTRACTED_STORAGE_BYTES + 1024
    allowed, msg = temp_tracker.check_can_extract(too_large)
    assert not allowed
    assert "storage budget" in msg.lower()


def test_kaggle_api_rate_limit_enforcement(temp_tracker):
    # Check initial
    allowed, msg = temp_tracker.check_can_api_request()
    assert allowed

    # Simulate 100 calls
    for _ in range(MAX_KAGGLE_API_REQUESTS):
        temp_tracker.record_api_request()

    # 101st call must be blocked
    allowed, msg = temp_tracker.check_can_api_request()
    assert not allowed
    assert "maximum kaggle api requests" in msg.lower()


def test_image_import_limit_enforcement(temp_tracker):
    # Process 50,000 images
    allowed, msg = temp_tracker.check_can_process_images(50000)
    assert allowed
    temp_tracker.record_images_processed(50000)

    # Another 60,000 images would exceed 100,000 cap
    allowed, msg = temp_tracker.check_can_process_images(60000)
    assert not allowed
    assert "maximum training images cap" in msg.lower()


def test_zip_slip_protection():
    dest_dir = os.path.abspath("/tmp/safe_dir")

    # Safe members
    assert is_safe_zip_path(dest_dir, "file.txt")
    assert is_safe_zip_path(dest_dir, "sub/dir/file.png")

    # Dangerous path traversal attacks
    assert not is_safe_zip_path(dest_dir, "../../../evil.bat")
    assert not is_safe_zip_path(dest_dir, "sub/../../evil.sh")

