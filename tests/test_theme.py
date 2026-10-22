"""Tests for Theme System and Dynamic CSS Generation in SignBridge."""
import re
from pathlib import Path


def test_app_theme_css_definitions():
    """Verify that app.py defines valid light and dark mode CSS variables and overrides."""
    root_dir = Path(__file__).resolve().parent.parent
    paths = [
        root_dir / "frontend" / "styles" / "theme.py",
        root_dir / "frontend" / "app.py",
        root_dir / "frontend" / "components" / "navbar.py",
        root_dir / "app.py",
    ]
    content = "\n".join(p.read_text(encoding="utf-8") for p in paths if p.exists())

    # Verify theme state initialization exists
    assert 'if "theme" not in st.session_state:' in content
    assert "def get_theme_css(theme: str) -> str:" in content

    # Verify both dark and light palette tokens exist
    required_tokens = [
        "--sb-bg",
        "--sb-surface",
        "--sb-surface-muted",
        "--sb-border",
        "--sb-text-main",
        "--sb-text-muted",
        "--sb-text-subtle",
        "--sb-primary",
        "--sb-success",
        "--sb-warning",
    ]
    for token in required_tokens:
        assert token in content, f"Missing token: {token}"

    # Verify theme toggle button exists in navbar
    assert 'key="theme_toggle_btn"' in content
    assert "def _toggle_theme():" in content

    # Verify anti-stale and camera protection rules
    assert 'div[data-stale="true"]' in content
    assert '[data-testid="stImage"] img' in content
    assert "filter: none !important;" in content


def test_creator_credits():
    """Verify that project creator credits are present and accurately credited."""
    root_dir = Path(__file__).resolve().parent.parent
    paths = [
        root_dir / "frontend" / "components" / "footer.py",
        root_dir / "frontend" / "pages" / "home.py",
        root_dir / "frontend" / "pages" / "about.py",
        root_dir / "app.py",
    ]
    content = "\n".join(p.read_text(encoding="utf-8") for p in paths if p.exists())

    assert "Made with care by" in content
    assert "Tushar Chauhan" in content
    assert "Ujjwal Dhiman" in content
    assert "A project by Tushar Chauhan and Ujjwal Dhiman" in content


def test_dark_and_light_palette_generation():
    """Verify that get_theme_css produces distinct, valid palettes for both dark and light modes."""
    from frontend.styles.theme import get_theme_css

    dark_css = get_theme_css("dark")
    light_css = get_theme_css("light")

    # Dark mode assertions
    assert "color-scheme: dark" in dark_css
    assert "--sb-bg: #0c0d10" in dark_css
    assert "--sb-text-main: #f4f5f8" in dark_css
    assert "--background-color: var(--sb-bg)" in dark_css
    assert "--text-color: var(--sb-text-main)" in dark_css
    assert '[data-testid="stSidebar"]' in dark_css
    assert 'div[data-testid="stMarkdownContainer"]' in dark_css
    assert 'div[data-testid="stToggle"]' in dark_css
    assert 'div[data-baseweb="select"]' in dark_css
    assert 'div[data-baseweb="popover"]' in dark_css
    assert 'div[data-testid="stAlert"]' in dark_css

    # Light mode assertions
    assert "color-scheme: light" in light_css
    assert "--sb-bg: #fbfaf8" in light_css
    assert "--sb-text-main: #141517" in light_css
    assert "--background-color: var(--sb-bg)" in light_css
    assert "--text-color: var(--sb-text-main)" in light_css


def test_theme_toggle_logic():
    """Verify that theme toggle correctly alternates between light and dark."""
    from frontend.components.navbar import _toggle_theme
    import streamlit as st

    # Simulate light theme
    st.session_state.theme = "light"
    _toggle_theme()
    assert st.session_state.theme == "dark"

    # Simulate dark theme
    _toggle_theme()
    assert st.session_state.theme == "light"


def test_light_mode_contrast_and_headings():
    """Verify that light mode palettes and key headings do not use hardcoded white text."""
    from frontend.styles.theme import get_theme_css

    light_css = get_theme_css("light")
    dark_css = get_theme_css("dark")

    # Gradients defined
    assert "--sb-heading-gradient" in light_css
    assert "--sb-brand-gradient" in light_css
    assert "--sb-metric-gradient" in light_css

    # Headings and cards use dynamic theme text variables
    assert ".sb-hero-title {" in light_css
    assert "background: var(--sb-heading-gradient)" in light_css
    assert ".sb-brand-name {" in light_css
    assert "background: var(--sb-brand-gradient)" in light_css
    assert ".sb-section-heading {" in light_css
    assert "color: var(--sb-text-main)" in light_css
