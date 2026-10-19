"""
Unit and Integration Tests for Offline English-to-Hindi Translation Feature.
Tests Helsinki-NLP/opus-mt-en-hi local execution, Devanagari script output,
graceful error handling, and UI integration points.
"""
from pathlib import Path
import pytest
from src.translator import EnglishToHindiTranslator, DEFAULT_MODEL_DIR


def is_devanagari(text: str) -> bool:
    """Check if string contains Devanagari characters (\u0900 - \u097F)."""
    return any("\u0900" <= char <= "\u097F" for char in text)


def test_translator_availability_and_structure():
    """Verify that the model directory and weight files exist locally for offline usage."""
    translator = EnglishToHindiTranslator(model_dir=DEFAULT_MODEL_DIR)
    assert translator.is_available, f"Model files missing at {DEFAULT_MODEL_DIR}"
    assert (DEFAULT_MODEL_DIR / "config.json").exists()
    assert (DEFAULT_MODEL_DIR / "source.spm").exists()
    assert (DEFAULT_MODEL_DIR / "target.spm").exists()
    assert (DEFAULT_MODEL_DIR / "model.safetensors").exists()


def test_translator_empty_and_whitespace_input():
    """Verify empty or blank inputs return empty translations without errors."""
    translator = EnglishToHindiTranslator(model_dir=DEFAULT_MODEL_DIR)
    res, err = translator.translate("")
    assert res == ""
    assert err is None

    res, err = translator.translate("   \n\t  ")
    assert res == ""
    assert err is None


def test_translator_missing_directory_handling(tmp_path):
    """Verify missing directory is handled gracefully without crashing."""
    empty_dir = tmp_path / "non_existent_model_dir"
    translator = EnglishToHindiTranslator(model_dir=empty_dir)
    assert not translator.is_available
    success, err = translator.load()
    assert not success
    assert "not found" in err.lower()

    res, trans_err = translator.translate("Hello")
    assert res is None
    assert "not found" in trans_err.lower()


def test_offline_translation_devanagari_sentences():
    """
    Test English-to-Hindi translation on canonical sentences:
    1. 'Hello, how are you?'
    2. 'I need help'
    3. 'Thank you'
    Verify all return valid Devanagari script without cloud API calls.
    """
    translator = EnglishToHindiTranslator(model_dir=DEFAULT_MODEL_DIR)
    success, err = translator.load()
    assert success, f"Failed to load model: {err}"
    assert translator.is_loaded

    test_cases = [
        ("Hello, how are you?", ["हैलो", "नमस्ते", "कैसे"]),
        ("I need help", ["मदद"]),
        ("Thank you", ["धन्यवाद", "शुक्रिया"]),
    ]

    for en_text, expected_keywords in test_cases:
        hi_text, trans_err = translator.translate(en_text)
        assert trans_err is None, f"Error translating '{en_text}': {trans_err}"
        assert hi_text is not None and len(hi_text) > 0
        assert is_devanagari(hi_text), f"Output '{hi_text}' should be in Devanagari script"
        assert any(kw in hi_text for kw in expected_keywords), (
            f"Expected one of {expected_keywords} in '{hi_text}'"
        )


def test_app_ui_translation_integration():
    """Verify that app.py integrates the translation button and session state."""
    root_dir = Path(__file__).resolve().parent.parent
    paths = [
        root_dir / "frontend" / "app.py",
        root_dir / "frontend" / "components" / "translation_card.py",
        root_dir / "frontend" / "components" / "sentence_controls.py",
        root_dir / "frontend" / "pages" / "live_app.py",
        root_dir / "app.py",
    ]
    content = "\n".join(p.read_text(encoding="utf-8") for p in paths if p.exists())

    assert "EnglishToHindiTranslator" in content
    assert 'get_translator()' in content
    assert 'translated_hindi_text' in content
    assert '"Translate to Hindi"' in content
    assert 'sb-translation-container' in content
    assert 'live_translate_btn' in content
    assert 'copy_hindi_btn' in content

