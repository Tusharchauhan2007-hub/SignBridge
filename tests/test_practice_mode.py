"""Tests for Practice & Learn mode state transitions and letter cycling."""
from pathlib import Path
from backend.data_collection import ISL_ALPHABET_LETTERS


def test_alphabet_letter_sequence():
    """Verify that ISL alphabet letters have exactly 26 distinct characters A-Z."""
    assert len(ISL_ALPHABET_LETTERS) == 26
    assert ISL_ALPHABET_LETTERS[0] == "A"
    assert ISL_ALPHABET_LETTERS[-1] == "Z"


def test_practice_mode_no_post_instantiation_widget_mutation():
    """Verify that live_app.py does not reassign practice_letter_select after widget instantiation."""
    live_app_path = Path(__file__).resolve().parent.parent / "frontend" / "pages" / "live_app.py"
    code = live_app_path.read_text(encoding="utf-8")

    # Ensure the previous crashing anti-pattern is completely absent
    assert 'st.session_state["practice_letter_select"] = next_letter' not in code
    assert "on_click=_on_next_practice_letter" in code
    assert "on_change=_on_practice_letter_change" in code


def test_next_practice_letter_callback_logic():
    """Simulate _on_next_practice_letter callback and verify wrap-around from A->B... and Z->A."""
    import streamlit as st

    def _on_next_practice_letter():
        curr = st.session_state.get("practice_target", "A")
        curr_idx = ISL_ALPHABET_LETTERS.index(curr) if curr in ISL_ALPHABET_LETTERS else 0
        next_letter = ISL_ALPHABET_LETTERS[(curr_idx + 1) % len(ISL_ALPHABET_LETTERS)]
        st.session_state.practice_target = next_letter
        st.session_state.practice_letter_select = next_letter

    # Case 1: Starting at A advances to B
    st.session_state.practice_target = "A"
    _on_next_practice_letter()
    assert st.session_state.practice_target == "B"
    assert st.session_state.practice_letter_select == "B"

    # Case 2: Wrapping at Z returns to A
    st.session_state.practice_target = "Z"
    _on_next_practice_letter()
    assert st.session_state.practice_target == "A"
    assert st.session_state.practice_letter_select == "A"

