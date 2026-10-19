"""
Hand tracking module for SignBridge.
Implements MediaPipe Tasks HandLandmarker with robust fallback, error handling,
and custom drawing utilities.
"""

import os
import urllib.request
from typing import List, Optional, Tuple, NamedTuple
import cv2
import numpy as np

try:
    import mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision
except ImportError as err:
    raise ImportError(
        "MediaPipe is not installed. Please install it using 'pip install mediapipe'."
    ) from err

# Official Google MediaPipe Hand Landmarker model URL
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)
DEFAULT_MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
DEFAULT_MODEL_PATH = os.path.join(DEFAULT_MODEL_DIR, "hand_landmarker.task")

# 21 Hand landmark connections (MediaPipe HandLandmarksConnections)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index finger
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle finger
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring finger
    (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
    (0, 17)                                 # Palm base
]


class Landmark(NamedTuple):
    x: float
    y: float
    z: float


class HandLandmarks(NamedTuple):
    landmarks: List[Landmark]
    handedness: str
    confidence: float


class HandDetectionResult(NamedTuple):
    hands: List[HandLandmarks]
    has_hand: bool
    annotated_image: Optional[np.ndarray] = None


class HandTracker:
    """MediaPipe Tasks HandLandmarker wrapper for real-time video and image detection."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        max_num_hands: int = 1,
        min_detection_confidence: float = 0.5,
        min_presence_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        self.model_path = model_path or DEFAULT_MODEL_PATH
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_presence_confidence = min_presence_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self._ensure_model_exists()
        self._init_detector()

    def _ensure_model_exists(self) -> None:
        """Download model if not present locally."""
        if not os.path.exists(self.model_path):
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            print(f"[SignBridge] Downloading HandLandmarker task model to {self.model_path}...")
            urllib.request.urlretrieve(MODEL_URL, self.model_path)
            print("[SignBridge] HandLandmarker task model downloaded successfully.")

    def _init_detector(self) -> None:
        """Initialize the HandLandmarker task detector."""
        base_options = mp_python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=self.max_num_hands,
            min_hand_detection_confidence=self.min_detection_confidence,
            min_hand_presence_confidence=self.min_presence_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame_bgr: np.ndarray) -> HandDetectionResult:
        """
        Detect hands in a BGR frame (from OpenCV).
        Returns HandDetectionResult containing detected hands and normalized landmarks.
        """
        if frame_bgr is None or frame_bgr.size == 0:
            return HandDetectionResult(hands=[], has_hand=False)

        # Convert OpenCV BGR to RGB
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        try:
            result = self.detector.detect(mp_image)
        except Exception as e:
            print(f"[SignBridge] Hand detection error: {e}")
            return HandDetectionResult(hands=[], has_hand=False)

        detected_hands: List[HandLandmarks] = []
        if result and result.hand_landmarks:
            for idx, hand_lms in enumerate(result.hand_landmarks):
                landmarks = [Landmark(x=lm.x, y=lm.y, z=lm.z) for lm in hand_lms]
                handedness = "Right"
                confidence = 1.0
                if result.handedness and idx < len(result.handedness) and result.handedness[idx]:
                    cat = result.handedness[idx][0]
                    handedness = cat.category_name or "Right"
                    confidence = float(cat.score) if hasattr(cat, "score") else 1.0

                detected_hands.append(
                    HandLandmarks(
                        landmarks=landmarks,
                        handedness=handedness,
                        confidence=confidence,
                    )
                )

        return HandDetectionResult(
            hands=detected_hands,
            has_hand=len(detected_hands) > 0,
        )

    def draw_landmarks(
        self,
        frame_bgr: np.ndarray,
        detection_result: HandDetectionResult,
        draw_bounding_box: bool = True,
    ) -> np.ndarray:
        """Draw hand skeleton connections and landmarks on frame."""
        if frame_bgr is None or not detection_result.has_hand:
            return frame_bgr

        annotated = frame_bgr.copy()
        height, width, _ = annotated.shape

        for hand in detection_result.hands:
            pts = []
            for lm in hand.landmarks:
                px = int(lm.x * width)
                py = int(lm.y * height)
                pts.append((px, py))

            # Draw connections (cyan/teal lines)
            for start_idx, end_idx in HAND_CONNECTIONS:
                if start_idx < len(pts) and end_idx < len(pts):
                    cv2.line(
                        annotated,
                        pts[start_idx],
                        pts[end_idx],
                        (230, 200, 40),  # BGR
                        2,
                        cv2.LINE_AA,
                    )

            # Draw landmark dots (white dot with blue rim)
            for idx, (px, py) in enumerate(pts):
                # Highlight wrist (index 0) and fingertips (4, 8, 12, 16, 20)
                if idx in (0, 4, 8, 12, 16, 20):
                    cv2.circle(annotated, (px, py), 6, (0, 140, 255), -1, cv2.LINE_AA)
                    cv2.circle(annotated, (px, py), 2, (255, 255, 255), -1, cv2.LINE_AA)
                else:
                    cv2.circle(annotated, (px, py), 4, (40, 220, 230), -1, cv2.LINE_AA)
                    cv2.circle(annotated, (px, py), 2, (255, 255, 255), -1, cv2.LINE_AA)

            # Draw optional bounding box and handedness badge
            if draw_bounding_box and pts:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                x_min, x_max = max(0, min(xs) - 15), min(width, max(xs) + 15)
                y_min, y_max = max(0, min(ys) - 15), min(height, max(ys) + 15)
                cv2.rectangle(annotated, (x_min, y_min), (x_max, y_max), (0, 200, 100), 2)
                badge_text = f"{hand.handedness} Hand ({int(hand.confidence * 100)}%)"
                cv2.putText(
                    annotated,
                    badge_text,
                    (x_min, max(20, y_min - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 120),
                    1,
                    cv2.LINE_AA,
                )

        return annotated

    def close(self) -> None:
        """Release MediaPipe resources."""
        if hasattr(self, "detector") and self.detector:
            try:
                self.detector.close()
            except Exception:
                pass

