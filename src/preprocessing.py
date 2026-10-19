"""
Compatibility shim for backend.preprocessing.
Directs imports to backend package.
"""

from backend.preprocessing import *
from backend.preprocessing import (
    NUM_LANDMARKS,
    NUM_COORDINATES,
    TOTAL_FEATURES,
    get_feature_names,
    LandmarkPreprocessor,
)

__all__ = [
    "NUM_LANDMARKS",
    "NUM_COORDINATES",
    "TOTAL_FEATURES",
    "get_feature_names",
    "LandmarkPreprocessor",
]
