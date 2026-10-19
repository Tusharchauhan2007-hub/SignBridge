"""
Unit tests for landmark preprocessing and normalization.
"""

import numpy as np
import pytest
from src.preprocessing import LandmarkPreprocessor, TOTAL_FEATURES, get_feature_names


class MockLandmark:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


@pytest.fixture
def preprocessor():
    return LandmarkPreprocessor(reference_joint=0, scale_joint=9)


@pytest.fixture
def sample_hand():
    """Generates synthetic 21 landmarks."""
    rng = np.random.RandomState(42)
    # 21 points in 3D
    pts = rng.uniform(0.2, 0.8, size=(21, 3)).astype(np.float32)
    # Ensure scale joint is not coincident with wrist
    pts[9] = pts[0] + np.array([0.0, 0.2, 0.0], dtype=np.float32)
    return pts


def test_feature_names_count():
    names = get_feature_names()
    assert len(names) == 63
    assert names[0] == "lm_0_x"
    assert names[-1] == "lm_20_z"


def test_normalized_output_shape(preprocessor, sample_hand):
    norm = preprocessor.normalize(sample_hand)
    assert norm.shape == (TOTAL_FEATURES,)
    assert norm.dtype == np.float32
    # Wrist coordinates in normalized space must be (0, 0, 0)
    assert pytest.approx(norm[0], abs=1e-5) == 0.0
    assert pytest.approx(norm[1], abs=1e-5) == 0.0
    assert pytest.approx(norm[2], abs=1e-5) == 0.0


def test_translation_invariance(preprocessor, sample_hand):
    """Translating the entire hand in 3D space should yield identical normalized features."""
    norm1 = preprocessor.normalize(sample_hand)
    shift = np.array([10.5, -25.2, 5.0], dtype=np.float32)
    shifted_hand = sample_hand + shift
    norm2 = preprocessor.normalize(shifted_hand)
    np.testing.assert_allclose(norm1, norm2, atol=1e-4)



def test_scale_invariance(preprocessor, sample_hand):
    """Uniformly scaling the hand size should yield identical normalized features."""
    wrist = sample_hand[0].copy()
    norm1 = preprocessor.normalize(sample_hand)

    # Scale relative to wrist
    scaled_hand = wrist + (sample_hand - wrist) * 2.5
    norm2 = preprocessor.normalize(scaled_hand)
    np.testing.assert_allclose(norm1, norm2, atol=1e-4)


def test_invalid_input_handling(preprocessor):
    # None input
    with pytest.raises(ValueError):
        preprocessor.normalize(None)

    # Wrong shape
    with pytest.raises(ValueError):
        preprocessor.normalize(np.zeros((10, 3)))

    # NaN coordinates
    bad_coords = np.zeros((21, 3))
    bad_coords[5, 1] = np.nan
    with pytest.raises(ValueError):
        preprocessor.normalize(bad_coords)

    # Inf coordinates
    bad_coords[5, 1] = np.inf
    with pytest.raises(ValueError):
        preprocessor.normalize(bad_coords)


def test_extract_from_landmarks(preprocessor):
    lms = [MockLandmark(float(i) * 0.01, float(i) * 0.02, 0.0) for i in range(21)]
    # Ensure point 9 is separated from 0
    lms[9] = MockLandmark(0.0, 0.2, 0.0)
    vec = preprocessor.extract_from_landmarks(lms)
    assert vec is not None
    assert len(vec) == 63
    # Too few landmarks
    assert preprocessor.extract_from_landmarks(lms[:15]) is None
