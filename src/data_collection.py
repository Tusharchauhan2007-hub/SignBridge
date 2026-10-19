"""
Compatibility shim for backend.data_collection.
Directs imports to backend package.
"""

from backend.data_collection import *
from backend.data_collection import (
    DatasetManager,
    CORE_ISL_GESTURES,
    ISL_ALPHABET_LETTERS,
    ALL_TARGET_CLASSES,
    ISL_ALPHABET_GUIDE,
    METADATA_COLUMNS,
    get_dataset_columns,
)

__all__ = [
    "DatasetManager",
    "CORE_ISL_GESTURES",
    "ISL_ALPHABET_LETTERS",
    "ALL_TARGET_CLASSES",
    "ISL_ALPHABET_GUIDE",
    "METADATA_COLUMNS",
    "get_dataset_columns",
]
