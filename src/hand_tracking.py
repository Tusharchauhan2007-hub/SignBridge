"""
Compatibility shim for backend.hand_tracking.
Directs imports to backend package.
"""

from backend.hand_tracking import *
from backend.hand_tracking import (
    HandTracker,
    Landmark,
    HandLandmarks,
    HandDetectionResult,
    HAND_CONNECTIONS,
    DEFAULT_MODEL_DIR,
    DEFAULT_MODEL_PATH,
)

__all__ = [
    "HandTracker",
    "Landmark",
    "HandLandmarks",
    "HandDetectionResult",
    "HAND_CONNECTIONS",
    "DEFAULT_MODEL_DIR",
    "DEFAULT_MODEL_PATH",
]
