"""
Unit tests for the SignPredictor inference engine and SentenceBuilder.
"""

import os
import numpy as np
import pytest
from sklearn.ensemble import RandomForestClassifier

from src.predictor import SignPredictor, PredictionResult
from src.text_to_speech import SentenceBuilder


def test_predictor_unloaded_handling():
    """Predictor should handle nonexistent model gracefully without crashing."""
    p = SignPredictor(model_path="nonexistent_model.joblib")
    assert not p.is_loaded
    res = p.predict(np.zeros(63))
    assert res.label == "Model not loaded"
    assert not res.is_valid


def test_predictor_no_hand_handling():
    """Predictor should return 'No hand detected' when hand feature is None."""
    p = SignPredictor()
    res = p.predict(None)
    assert res.label == "No hand detected"
    assert res.confidence == 0.0
    assert not res.is_valid


def test_confidence_threshold_gating():
    """When confidence is below threshold, prediction should be rejected."""
    p = SignPredictor(confidence_threshold=0.99)  # Ultra-high threshold
    # Even if loaded, an ambiguous vector should fall below 0.99
    res = p.predict(np.random.normal(0, 1, 63))
    if p.is_loaded:
        assert res.label in ("Sign not recognized", "Stabilizing...")
        assert not res.is_valid


def test_temporal_smoothing_buffer():
    """Predictor should stabilize over rolling window."""
    p = SignPredictor(smoothing_window_size=5, agreement_ratio=0.6)
    p.reset_history()
    assert len(p.history) == 0
    # Simulate adding non-hand
    p.predict(None)
    assert len(p.history) == 1
    assert p.history[-1] == "NO_HAND"


def test_sentence_builder_cooldown():
    """SentenceBuilder should avoid duplicate spam within cooldown window."""
    sb = SentenceBuilder(cooldown_seconds=1.0)
    assert sb.append_token("HELLO")
    assert sb.get_text() == "HELLO"

    # Immediate second append of identical token should be debounced
    assert not sb.append_token("HELLO")
    assert sb.get_text() == "HELLO"

    # Different token can be appended immediately
    assert sb.append_token("YES")
    assert sb.get_text() == "HELLO YES"


def test_sentence_builder_operations():
    """Test space, backspace, and clear operations."""
    sb = SentenceBuilder()
    sb.append_token("HELLO")
    sb.append_space()
    sb.append_token("HELP")
    assert sb.get_text() == "HELLO HELP"

    # Backspace removes 'P'
    sb.backspace()
    assert sb.get_text() == "HELLO HEL"

    # Repeated backspaces delete remainder of HELP
    sb.backspace()  # removes 'L'
    sb.backspace()  # removes 'E'
    sb.backspace()  # removes 'H'
    assert sb.get_text() == "HELLO "

    # Backspace removes space
    sb.backspace()
    assert sb.get_text() == "HELLO"

    # Clear empties sentence
    sb.clear()
    assert sb.get_text() == ""


def test_sentence_builder_letters_fingerspelling():
    """Test fingerspelling letters concatenation into words with spaces."""
    sb = SentenceBuilder(cooldown_seconds=0.01)
    # Spell C-A-T
    for letter in ["C", "A", "T"]:
        sb.append_token(letter)
    assert sb.get_text() == "CAT"

    # Insert space
    sb.append_space()

    # Spell D-O-G
    for letter in ["D", "O", "G"]:
        sb.append_token(letter)
    assert sb.get_text() == "CAT DOG"

    # Append word sign with underscore
    sb.append_token("THANK_YOU")
    assert sb.get_text() == "CAT DOG THANK YOU"

    # Backspace removes last character 'U'
    sb.backspace()
    assert sb.get_text() == "CAT DOG THANK YO"


def test_space_and_clear_requirements():
    """
    Test the exact 7 user-specified scenarios for Space and Clear:
    1. Adding letters H, E, L, L, O produces HELLO.
    2. Clicking Space produces 'HELLO '.
    3. Clicking Space again produces 'HELLO  ' (two trailing spaces).
    4. Adding W, O, R, L, D after spaces produces 'HELLO  WORLD'.
    5. Clicking Clear Text completely clears the text ("").
    6. After clicking Clear Text, the text stays cleared and does not immediately
       re-append the letter or gesture currently in front of the camera on the next frame.
    7. Clicking Space on an empty text buffer produces ' '.
    """
    # Scenario 7: Space on an empty buffer produces ' '
    sb_empty = SentenceBuilder()
    sb_empty.append_space()
    assert sb_empty.get_text() == " "

    # Scenario 1: Adding H, E, L, L, O produces HELLO
    sb = SentenceBuilder(cooldown_seconds=0.01)
    sb.append_token("H")
    sb.append_token("E")
    sb.append_token("L")
    sb.append_token("L", force=True)  # double letter
    sb.append_token("O")
    assert sb.get_text() == "HELLO"

    # Scenario 2: Clicking Space produces 'HELLO '
    sb.append_space()
    assert sb.get_text() == "HELLO "

    # Scenario 3: Clicking Space again produces 'HELLO  '
    sb.append_space()
    assert sb.get_text() == "HELLO  "

    # Scenario 4: Adding W, O, R, L, D produces 'HELLO  WORLD'
    sb.append_token("W")
    sb.append_token("O")
    sb.append_token("R")
    sb.append_token("L")
    sb.append_token("D")
    assert sb.get_text() == "HELLO  WORLD"

    # Scenario 5: Clicking Clear Text completely clears the text ("")
    sb.clear(current_sign="D")
    assert sb.get_text() == ""

    # Scenario 6: Camera loop frame 1 with 'D' held in front of camera does not re-append
    assert not sb.can_append("D")
    assert not sb.append_token("D", force=False)
    assert sb.get_text() == ""

    # Lowering hand releases suppression
    sb.notify_no_hand()
    # Now user raises 'D' again or signs a new gesture
    assert sb.can_append("D")
    assert sb.append_token("D")
    assert sb.get_text() == "D"


def test_delete_button_requirements():
    """
    Test user-specified Delete button requirements:
    1. Text 'HELLO' becomes 'HELL' after one click.
    2. Text 'H' becomes empty after one click.
    3. Clicking Delete with empty text does not crash.
    4. Repeated clicks delete one character per click:
       'HELLO' -> 'HELL' -> 'HEL' -> 'HE' -> 'H' -> ''
    5. 'HH' becomes 'H' after one click, and '' after second click.
    6. Suppression of the held sign prevents immediate auto-add re-addition.
    """
    # 1. HELLO -> HELL
    sb = SentenceBuilder(cooldown_seconds=0.01)
    sb.append_token("HELLO")
    assert sb.get_text() == "HELLO"
    sb.backspace()
    assert sb.get_text() == "HELL"

    # 4. Repeated clicks: HELL -> HEL -> HE -> H -> empty
    sb.backspace()
    assert sb.get_text() == "HEL"
    sb.backspace()
    assert sb.get_text() == "HE"
    sb.backspace()
    assert sb.get_text() == "H"
    sb.backspace()
    assert sb.get_text() == ""

    # 3. Empty text: do nothing without exception
    sb.backspace()
    assert sb.get_text() == ""

    # 2. Text H becomes empty after one click
    sb_h = SentenceBuilder()
    sb_h.append_token("H")
    assert sb_h.get_text() == "H"
    sb_h.backspace()
    assert sb_h.get_text() == ""

    # 5. HH -> H -> empty
    sb_hh = SentenceBuilder(cooldown_seconds=0.01)
    sb_hh.append_token("H")
    sb_hh.append_token("H", force=True)
    assert sb_hh.get_text() == "HH"
    sb_hh.backspace(current_sign="H")
    assert sb_hh.get_text() == "H"
    # Auto-add should be suppressed while 'H' is still held in front of camera
    assert not sb_hh.can_append("H")
    sb_hh.backspace(current_sign="H")
    assert sb_hh.get_text() == ""



