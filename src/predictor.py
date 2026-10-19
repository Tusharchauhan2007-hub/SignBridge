"""
Compatibility shim for backend.predictor.
Directs imports to backend package.
"""

from backend.predictor import *
from backend.predictor import (
    PredictionResult,
    SignPredictor,
    DEFAULT_MODEL_DIR,
    DEFAULT_MODEL_FILE,
)

__all__ = [
    "PredictionResult",
    "SignPredictor",
    "DEFAULT_MODEL_DIR",
    "DEFAULT_MODEL_FILE",
]
