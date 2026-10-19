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

