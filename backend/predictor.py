"""
Prediction engine for SignBridge.
Loads the trained Random Forest artifact, performs inference on normalized landmark features,
applies confidence thresholding and temporal window smoothing to prevent flickering,
and outputs standardized PredictionResult objects.
"""

from collections import Counter, deque
import os
import sys
from typing import Dict, List, Optional, Tuple, NamedTuple

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import joblib
import numpy as np


try:
    from backend.preprocessing import TOTAL_FEATURES
except ImportError:
    from src.preprocessing import TOTAL_FEATURES

DEFAULT_MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
DEFAULT_MODEL_FILE = os.path.join(DEFAULT_MODEL_DIR, "isl_classifier.joblib")


class PredictionResult(NamedTuple):
    label: str
    raw_label: str
    confidence: float
    is_valid: bool
    probabilities: Dict[str, float]
    status_message: str


class SignPredictor:
    """
    Gesture classification predictor with temporal smoothing and confidence gating.
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        confidence_threshold: float = 0.60,
        smoothing_window_size: int = 7,
        agreement_ratio: float = 0.55,
    ):
        self.model_path = model_path or DEFAULT_MODEL_FILE
        self.confidence_threshold = confidence_threshold
        self.smoothing_window_size = smoothing_window_size
        self.agreement_ratio = agreement_ratio

        self.model = None
        self.classes: List[str] = []
        self.metadata: Dict = {}
        self.history: deque = deque(maxlen=smoothing_window_size)
        self.conf_history: deque = deque(maxlen=smoothing_window_size)

        self.load_model()

    def load_model(self, path: Optional[str] = None) -> bool:
        """Load trained model artifact from joblib file."""
        target_path = path or self.model_path
        if not os.path.exists(target_path):
            self.model = None
            self.classes = []
            return False

        try:
            artifact = joblib.load(target_path)
            if isinstance(artifact, dict) and "model" in artifact:
                self.model = artifact["model"]
                self.classes = list(artifact.get("classes", []))
                self.metadata = artifact
            else:
                self.model = artifact
                self.classes = list(getattr(self.model, "classes_", []))
                self.metadata = {}
            self.reset_history()
            return True
        except Exception as e:
            print(f"[SignBridge] Failed to load model artifact: {e}")
            self.model = None
            self.classes = []
            return False

    @property
    def is_loaded(self) -> bool:
        """Return True if a trained classification model is ready."""
        return self.model is not None and len(self.classes) > 0

    def reset_history(self) -> None:
        """Clear temporal smoothing buffers."""
        self.history.clear()
        self.conf_history.clear()

    def predict(self, features: Optional[np.ndarray]) -> PredictionResult:
        """
        Predict sign from a 63-dimensional normalized feature vector.
        Handles no-hand detection, below-confidence fallbacks, and window smoothing.
        """
        # 1. No hand detected
        if features is None:
            self.history.append("NO_HAND")
            self.conf_history.append(0.0)
            return PredictionResult(
                label="No hand detected",
                raw_label="NO_HAND",
                confidence=0.0,
                is_valid=False,
                probabilities={},
                status_message="Place your hand clearly within the camera frame.",
            )

        # 2. Model not loaded
        if not self.is_loaded:
            return PredictionResult(
                label="Model not loaded",
                raw_label="UNLOADED",
                confidence=0.0,
                is_valid=False,
                probabilities={},
                status_message="No trained model found. Please train a model in the Training page first.",
            )

        # 3. Shape validation
        feat_arr = np.asarray(features, dtype=np.float32).flatten()
        if feat_arr.size != TOTAL_FEATURES:
            return PredictionResult(
                label="Feature error",
                raw_label="ERROR",
                confidence=0.0,
                is_valid=False,
                probabilities={},
                status_message=f"Expected {TOTAL_FEATURES} features, got {feat_arr.size}.",
            )

        # 4. Instantaneous Inference
        probs = self.model.predict_proba([feat_arr])[0]
        max_idx = int(np.argmax(probs))
        raw_confidence = float(probs[max_idx])
        raw_pred = str(self.classes[max_idx])

        # Create sorted probabilities dictionary
        prob_dict = {
            str(cls): float(prob)
            for cls, prob in sorted(zip(self.classes, probs), key=lambda x: x[1], reverse=True)
        }

        # 5. Confidence Threshold Gating
        if raw_confidence < self.confidence_threshold:
            self.history.append("UNCERTAIN")
            self.conf_history.append(raw_confidence)
            return PredictionResult(
                label="Sign not recognized",
                raw_label=raw_pred,
                confidence=raw_confidence,
                is_valid=False,
                probabilities=prob_dict,
                status_message=f"Confidence ({int(raw_confidence * 100)}%) is below threshold ({int(self.confidence_threshold * 100)}%).",
            )

        # Record valid prediction in smoothing window
        self.history.append(raw_pred)
        self.conf_history.append(raw_confidence)

        # 6. Temporal Window Smoothing (Majority Voting)
        recent_valid = [lbl for lbl in self.history if lbl not in ("NO_HAND", "UNCERTAIN")]
        if not recent_valid:
            return PredictionResult(
                label="Sign not recognized",
                raw_label=raw_pred,
                confidence=raw_confidence,
                is_valid=False,
                probabilities=prob_dict,
                status_message="Stabilizing prediction...",
            )

        counts = Counter(recent_valid)
        most_common_label, count = counts.most_common(1)[0]
        required_votes = max(1, int(len(self.history) * self.agreement_ratio))

        if count >= required_votes:
            smoothed_label = most_common_label
            # Average confidence of the winning class in the window
            smoothed_conf = float(np.mean(list(self.conf_history)))
            return PredictionResult(
                label=smoothed_label,
                raw_label=raw_pred,
                confidence=smoothed_conf,
                is_valid=True,
                probabilities=prob_dict,
                status_message="Recognized with high confidence.",
            )
        else:
            return PredictionResult(
                label="Stabilizing...",
                raw_label=raw_pred,
                confidence=raw_confidence,
                is_valid=False,
                probabilities=prob_dict,
                status_message="Hold hand steady to confirm sign.",
            )
