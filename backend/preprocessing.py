"""
Preprocessing module for SignBridge.
Transforms raw 21 MediaPipe hand landmarks (x, y, z) into a translation-invariant
and scale-normalized 63-dimensional feature vector.
"""

from typing import List, Optional, Union
import numpy as np


NUM_LANDMARKS = 21
NUM_COORDINATES = 3
TOTAL_FEATURES = NUM_LANDMARKS * NUM_COORDINATES  # 63


def get_feature_names() -> List[str]:
    """Generate standardized column names for the 63 landmark features."""
    names = []
    for i in range(NUM_LANDMARKS):
        for axis in ("x", "y", "z"):
            names.append(f"lm_{i}_{axis}")
    return names


class LandmarkPreprocessor:
    """
    Handles landmark normalization and feature vector extraction.
    Normalization approach:
      1. Translation Invariance: Shift all coordinates relative to wrist (Landmark 0).
      2. Scale Invariance: Divide coordinates by the Euclidean distance between
         wrist (0) and middle finger MCP joint (9), with safety epsilon.
    """

    def __init__(self, reference_joint: int = 0, scale_joint: int = 9):
        self.reference_joint = reference_joint
        self.scale_joint = scale_joint

    def normalize(self, coords: np.ndarray) -> np.ndarray:
        """
        Normalize coordinate array of shape (21, 3) or (63,).
        Returns normalized 1D float32 array of shape (63,).
        """
        if coords is None:
            raise ValueError("Input coordinates cannot be None.")

        coords_arr = np.asarray(coords, dtype=np.float32)

        if coords_arr.size != TOTAL_FEATURES:
            raise ValueError(
                f"Expected {TOTAL_FEATURES} coordinate values (21 landmarks x 3 axes), "
                f"but received {coords_arr.size} values."
            )

        if np.isnan(coords_arr).any() or np.isinf(coords_arr).any():
            raise ValueError("Landmark coordinates contain NaN or Inf values.")

        points = coords_arr.reshape((NUM_LANDMARKS, NUM_COORDINATES)).astype(np.float64)

        # 1. Wrist-relative translation
        ref_point = points[self.reference_joint].copy()
        translated = points - ref_point

        # 2. Scale normalization (wrist to middle MCP joint distance)
        scale_dist = np.linalg.norm(points[self.scale_joint] - ref_point)
        if scale_dist < 1e-4:
            # Fallback to maximum distance from wrist if middle MCP is too close
            scale_dist = np.max(np.linalg.norm(translated, axis=1))
            if scale_dist < 1e-4:
                scale_dist = 1.0  # Avoid division by zero for collapsed points

        normalized = translated / scale_dist
        return normalized.flatten().astype(np.float32)


    def extract_from_landmarks(self, landmarks) -> Optional[np.ndarray]:
        """
        Extract and normalize feature vector from a list of MediaPipe landmark objects
        or NamedTuple objects with attributes .x, .y, .z.
        """
        if not landmarks or len(landmarks) != NUM_LANDMARKS:
            return None

        raw = np.zeros((NUM_LANDMARKS, NUM_COORDINATES), dtype=np.float32)
        for i, lm in enumerate(landmarks):
            if hasattr(lm, "x") and hasattr(lm, "y") and hasattr(lm, "z"):
                raw[i, 0] = lm.x
                raw[i, 1] = lm.y
                raw[i, 2] = lm.z
            elif isinstance(lm, (list, tuple)) and len(lm) >= 3:
                raw[i, 0] = lm[0]
                raw[i, 1] = lm[1]
                raw[i, 2] = lm[2]
            else:
                return None

        return self.normalize(raw)
