"""
SignBridge — Central Configuration & Hard Resource Limits.
Enforces strict 100% free-only policy and hard budget caps across all operations:
- Zero paid API usage, zero charges, zero paid cloud services.
- Hard limits for download size, extracted storage, image count, API calls, training time, and RAM.
"""

import json
import os
import shutil
import sys
from typing import Any, Dict, Optional, Tuple

# Base Project Paths
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
RAW_DATASETS_DIR = os.path.join(DATA_DIR, "raw_datasets")
EXTRACTED_DATASETS_DIR = os.path.join(DATA_DIR, "extracted_datasets")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "isl_dataset.csv")
MANIFEST_PATH = os.path.join(DATA_DIR, "dataset_manifest.json")
RESOURCE_USAGE_PATH = os.path.join(DATA_DIR, "resource_usage.json")

# =============================================================================
# HARD RESOURCE BUDGET LIMITS (Strictly Enforced — Never Silently Raised)
# =============================================================================
MAX_TOTAL_DOWNLOAD_BYTES: int = 2 * 1024 * 1024 * 1024       # 2 GB Hard Cap
MAX_EXTRACTED_STORAGE_BYTES: int = 5 * 1024 * 1024 * 1024   # 5 GB Hard Cap
MAX_DATASETS: int = 10                                       # Max 10 datasets
MAX_TRAINING_IMAGES: int = 100_000                           # Max 100,000 images
MAX_DOWNLOAD_RETRIES: int = 2                                # Max 2 retries per dataset
MAX_KAGGLE_API_REQUESTS: int = 100                           # Max 100 API calls per project run
MAX_TRAINING_TIME_SECONDS: int = 60 * 60                     # 60 Minutes per training run
MAX_LOCAL_RAM_BYTES: int = 4 * 1024 * 1024 * 1024            # 4 GB RAM target limit

# Minimum disk safety buffer (prevent filling system drive)
MIN_FREE_DISK_BUFFER_BYTES: int = 1 * 1024 * 1024 * 1024     # 1 GB safety buffer


class BudgetExceededError(Exception):
    """Raised when an operation would exceed any configured hard limit."""
    pass


class ResourceBudgetTracker:
    """
    Cumulative tracker and enforcer for project resource consumption.
    Saves and reads state from data/resource_usage.json.
    """

    def __init__(self, usage_path: Optional[str] = None):
        self.usage_path = usage_path or RESOURCE_USAGE_PATH
        self._ensure_initialized()

    def _ensure_initialized(self) -> None:
        os.makedirs(os.path.dirname(self.usage_path), exist_ok=True)
        if not os.path.exists(self.usage_path) or os.path.getsize(self.usage_path) == 0:
            initial_state = {
                "total_downloaded_bytes": 0,
                "total_extracted_bytes": 0,
                "total_datasets_downloaded": 0,
                "total_images_processed": 0,
                "total_kaggle_api_requests": 0,
                "datasets": {},
            }
            self._save(initial_state)

    def _load(self) -> Dict[str, Any]:
        try:
            with open(self.usage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "total_downloaded_bytes": 0,
                "total_extracted_bytes": 0,
                "total_datasets_downloaded": 0,
                "total_images_processed": 0,
                "total_kaggle_api_requests": 0,
                "datasets": {},
            }

    def _save(self, state: Dict[str, Any]) -> None:
        with open(self.usage_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def get_summary(self) -> Dict[str, Any]:
        """Returns current resource usage metrics and remaining budget."""
        state = self._load()
        free_disk = shutil.disk_usage(DATA_DIR).free if os.path.exists(DATA_DIR) else shutil.disk_usage(PROJECT_ROOT).free
        return {
            "downloaded_bytes": state.get("total_downloaded_bytes", 0),
            "downloaded_mb": round(state.get("total_downloaded_bytes", 0) / (1024 * 1024), 2),
            "max_download_mb": round(MAX_TOTAL_DOWNLOAD_BYTES / (1024 * 1024), 2),
            "remaining_download_mb": round((MAX_TOTAL_DOWNLOAD_BYTES - state.get("total_downloaded_bytes", 0)) / (1024 * 1024), 2),
            "extracted_bytes": state.get("total_extracted_bytes", 0),
            "extracted_mb": round(state.get("total_extracted_bytes", 0) / (1024 * 1024), 2),
            "max_extracted_mb": round(MAX_EXTRACTED_STORAGE_BYTES / (1024 * 1024), 2),
            "datasets_downloaded": state.get("total_datasets_downloaded", 0),
            "max_datasets": MAX_DATASETS,
            "images_processed": state.get("total_images_processed", 0),
            "max_images": MAX_TRAINING_IMAGES,
            "api_requests": state.get("total_kaggle_api_requests", 0),
            "max_api_requests": MAX_KAGGLE_API_REQUESTS,
            "available_disk_gb": round(free_disk / (1024 * 1024 * 1024), 2),
        }

    def check_can_download(self, size_bytes: Optional[int]) -> Tuple[bool, str]:
        """Verifies whether a download of size_bytes is permitted within limits."""
        state = self._load()
        if size_bytes is None or size_bytes <= 0:
            return False, "Cannot download: Dataset size is unknown or unbounded."

        # Check total datasets count
        if state.get("total_datasets_downloaded", 0) >= MAX_DATASETS:
            return False, f"Hard limit reached: Maximum datasets count ({MAX_DATASETS}) reached."

        # Check download budget
        new_total = state.get("total_downloaded_bytes", 0) + size_bytes
        if new_total > MAX_TOTAL_DOWNLOAD_BYTES:
            req_mb = round(size_bytes / (1024 * 1024), 2)
            rem_mb = round((MAX_TOTAL_DOWNLOAD_BYTES - state.get("total_downloaded_bytes", 0)) / (1024 * 1024), 2)
            return False, f"Hard limit reached: Download of {req_mb} MB exceeds remaining budget of {rem_mb} MB (Max {MAX_TOTAL_DOWNLOAD_BYTES // (1024*1024*1024)} GB)."

        # Check local disk capacity
        target_dir = RAW_DATASETS_DIR if os.path.exists(RAW_DATASETS_DIR) else PROJECT_ROOT
        free_disk = shutil.disk_usage(target_dir).free
        if free_disk < (size_bytes + MIN_FREE_DISK_BUFFER_BYTES):
            return False, f"Insufficient disk space: {round(free_disk/(1024*1024), 1)} MB free; requires {round((size_bytes+MIN_FREE_DISK_BUFFER_BYTES)/(1024*1024), 1)} MB with safety buffer."

        return True, "Download permitted within budget."

    def record_download(self, dataset_id: str, size_bytes: int, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Records a completed download in the persistent state."""
        state = self._load()
        state["total_downloaded_bytes"] = state.get("total_downloaded_bytes", 0) + size_bytes
        state["total_datasets_downloaded"] = state.get("total_datasets_downloaded", 0) + 1
        if "datasets" not in state:
            state["datasets"] = {}
        state["datasets"][dataset_id] = {
            "download_size_bytes": size_bytes,
            "downloaded": True,
            "metadata": metadata or {},
        }
        self._save(state)

    def check_can_extract(self, expected_bytes: int) -> Tuple[bool, str]:
        """Verifies whether archive extraction fits within storage and disk limits."""
        state = self._load()
        new_total = state.get("total_extracted_bytes", 0) + expected_bytes
        if new_total > MAX_EXTRACTED_STORAGE_BYTES:
            req_mb = round(expected_bytes / (1024 * 1024), 2)
            rem_mb = round((MAX_EXTRACTED_STORAGE_BYTES - state.get("total_extracted_bytes", 0)) / (1024 * 1024), 2)
            return False, f"Hard limit reached: Extraction of {req_mb} MB exceeds remaining extracted storage budget of {rem_mb} MB (Max {MAX_EXTRACTED_STORAGE_BYTES // (1024*1024*1024)} GB)."

        target_dir = EXTRACTED_DATASETS_DIR if os.path.exists(EXTRACTED_DATASETS_DIR) else PROJECT_ROOT
        free_disk = shutil.disk_usage(target_dir).free
        if free_disk < (expected_bytes + MIN_FREE_DISK_BUFFER_BYTES):
            return False, "Insufficient free disk space for safe extraction."

        return True, "Extraction permitted within budget."

    def record_extraction(self, dataset_id: str, extracted_bytes: int) -> None:
        """Records extracted storage consumption."""
        state = self._load()
        state["total_extracted_bytes"] = state.get("total_extracted_bytes", 0) + extracted_bytes
        if "datasets" not in state:
            state["datasets"] = {}
        if dataset_id in state["datasets"]:
            state["datasets"][dataset_id]["extracted_bytes"] = extracted_bytes
        self._save(state)

    def check_can_api_request(self) -> Tuple[bool, str]:
        """Checks Kaggle API call count cap (Max 100)."""
        state = self._load()
        calls = state.get("total_kaggle_api_requests", 0)
        if calls >= MAX_KAGGLE_API_REQUESTS:
            return False, f"Hard limit reached: Maximum Kaggle API requests ({MAX_KAGGLE_API_REQUESTS}) reached for this project run."
        return True, "API request permitted."

    def record_api_request(self) -> None:
        """Increments API request count."""
        state = self._load()
        state["total_kaggle_api_requests"] = state.get("total_kaggle_api_requests", 0) + 1
        self._save(state)

    def check_can_process_images(self, count: int) -> Tuple[bool, str]:
        """Checks if importing count images remains under 100,000 image limit."""
        state = self._load()
        current = state.get("total_images_processed", 0)
        if current + count > MAX_TRAINING_IMAGES:
            return False, f"Hard limit reached: Adding {count} images would exceed maximum training images cap ({MAX_TRAINING_IMAGES}). Currently processed: {current}."
        return True, "Image processing permitted."

    def record_images_processed(self, count: int) -> None:
        """Records number of processed images."""
        state = self._load()
        state["total_images_processed"] = state.get("total_images_processed", 0) + count
        self._save(state)

