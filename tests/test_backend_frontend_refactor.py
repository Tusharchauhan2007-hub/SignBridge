"""
Tests verifying clean separation and interoperability of frontend and backend packages.
"""

from pathlib import Path
import numpy as np


def test_backend_exports_and_functionality():
    """Verify backend modules import and execute properly."""
    import backend
    from backend.preprocessing import LandmarkPreprocessor, TOTAL_FEATURES, get_feature_names
    from backend.data_collection import DatasetManager, CORE_ISL_GESTURES, ISL_ALPHABET_LETTERS
    from backend.hand_tracking import HandTracker
    from backend.predictor import SignPredictor
    from backend.text_to_speech import SentenceBuilder
    from backend.train_model import ModelTrainer
    from backend.translator import EnglishToHindiTranslator

    assert TOTAL_FEATURES == 63
    assert len(get_feature_names()) == 63
    preprocessor = LandmarkPreprocessor()
    dummy_coords = np.zeros((21, 3), dtype=np.float32)
    norm = preprocessor.normalize(dummy_coords)
    assert norm.shape == (63,)

    assert len(CORE_ISL_GESTURES) == 5
    assert len(ISL_ALPHABET_LETTERS) == 26

    sb = SentenceBuilder()
    sb.append_token("H")
    sb.append_token("I")
    assert sb.get_text() == "HI"
    sb.clear()
    assert sb.get_text() == ""

    predictor = SignPredictor()
    assert hasattr(predictor, "predict")

    translator = EnglishToHindiTranslator()
    assert hasattr(translator, "translate")

    tracker = HandTracker(max_num_hands=1)
    res = tracker.detect(np.zeros((240, 320, 3), dtype=np.uint8))
    assert res.has_hand is False
    assert len(res.hands) == 0


def test_frontend_exports_and_structure():
    """Verify frontend styling, components, and pages exist and are importable."""
    from frontend.styles.theme import get_theme_css
    from frontend.components.navbar import _toggle_theme, render_navbar
    from frontend.components.footer import render_footer
    from frontend.components.onboarding import render_onboarding_guide
    from frontend.components.translation_card import render_translation_display
    from frontend.components.sentence_controls import render_sentence_controls
    from frontend.components.telemetry import render_positioning_tips
    from frontend.pages.home import render_home_page
    from frontend.pages.how_it_works import render_how_it_works_page
    from frontend.pages.features import render_features_page
    from frontend.pages.live_app import render_live_app_page
    from frontend.pages.studio import render_studio_page
    from frontend.pages.about import render_about_page

    light_css = get_theme_css("light")
    dark_css = get_theme_css("dark")
    assert "--sb-bg" in light_css
    assert "--sb-bg" in dark_css
    assert callable(render_navbar)
    assert callable(render_footer)
    assert callable(render_live_app_page)


def test_src_backwards_compatibility_shims():
    """Verify that legacy src imports still work cleanly."""
    from src.preprocessing import LandmarkPreprocessor as Pre_Src
    from backend.preprocessing import LandmarkPreprocessor as Pre_Back
    assert Pre_Src is Pre_Back

    from src.predictor import SignPredictor as Pred_Src
    from backend.predictor import SignPredictor as Pred_Back
    assert Pred_Src is Pred_Back

    from src.text_to_speech import SentenceBuilder as SB_Src
    from backend.text_to_speech import SentenceBuilder as SB_Back
    assert SB_Src is SB_Back

    from src.data_collection import DatasetManager as DM_Src
    from backend.data_collection import DatasetManager as DM_Back
    assert DM_Src is DM_Back

    from src.translator import EnglishToHindiTranslator as TR_Src
    from backend.translator import EnglishToHindiTranslator as TR_Back
    assert TR_Src is TR_Back


def test_app_and_frontend_importable_without_premature_execution():
    """Verify that importing app and frontend.app does not crash or execute main prematurely."""
    import importlib
    import app
    assert hasattr(app, "main")
    assert callable(app.main)

    from frontend import app as frontend_app
    assert hasattr(frontend_app, "main")
    assert callable(frontend_app.main)

