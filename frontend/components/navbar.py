"""
Navigation bar and theme toggle component for SignBridge.
Refined dark-tech layout with geometric branding, status chips, and responsive navigation.
Guaranteed safe theme initialization and active route highlighting.
"""

import streamlit as st


def _ensure_theme() -> str:
    """Safely ensure theme exists in session state with 'dark' default."""
    if "theme" not in st.session_state:
        try:
            q_theme = st.query_params.get("theme", None)
            st.session_state.theme = q_theme if q_theme in ("light", "dark") else "dark"
        except Exception:
            st.session_state.theme = "dark"
    return st.session_state.theme


def _toggle_theme():
    """Toggles between light and dark theme mode and persists in query params."""
    curr = st.session_state.get("theme", "dark")
    nxt = "dark" if curr == "light" else "light"
    st.session_state.theme = nxt
    try:
        st.query_params["theme"] = nxt
    except Exception:
        pass


def render_navbar() -> None:
    """Renders the top branding bar, system status chip, and page navigation buttons."""
    theme = _ensure_theme()
    is_dark = (theme == "dark")

    nav_top_col, nav_theme_col = st.columns([4.4, 1.2])
    with nav_top_col:
        st.markdown(
            """
            <div class="sb-navbar" style="margin-bottom:0;">
                <div class="sb-brand">
                    <div class="sb-brand-logo">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <rect x="2" y="2" width="20" height="20" rx="6" stroke="#6366f1" stroke-width="1.8"/>
                            <path d="M7 16L17 8" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
                            <path d="M9 8H17V16" stroke="#06b6d4" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    </div>
                    <span class="sb-brand-name">SignBridge</span>
                    <div class="sb-status-chip" style="margin-left: 0.35rem;">
                        <span class="sb-status-dot sb-dot-ready"></span>
                        <span>ONLINE // ISL 2026</span>
                    </div>
                </div>
                <div class="sb-nav-tagline">
                    Assistive Computer Vision • Offline Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with nav_theme_col:
        theme_btn_label = "☀️ Light View" if is_dark else "🌙 Dark Tech View"
        if st.button(
            theme_btn_label,
            key="theme_toggle_btn",
            use_container_width=True,
            on_click=_toggle_theme,
        ):
            st.rerun()

    active_page = st.session_state.get("active_page", "Home")
    live_mode = st.session_state.get("live_mode_view", "Live Recognition")
    is_live_active = (active_page == "Live App" and live_mode == "Live Recognition")
    is_practice_active = (active_page == "Live App" and live_mode == "Interactive Practice Mode")

    # Navigation Menu Buttons with Active State Highlighting
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6, nav_col7 = st.columns([1, 1.15, 1, 1.35, 1, 0.9, 1.35])

    with nav_col1:
        if st.button("Home", key="nav_home", use_container_width=True, type="secondary" if active_page != "Home" else "primary"):
            st.session_state.active_page = "Home"
            st.rerun()

    with nav_col2:
        if st.button("How It Works", key="nav_how", use_container_width=True, type="secondary" if active_page != "How It Works" else "primary"):
            st.session_state.active_page = "How It Works"
            st.rerun()

    with nav_col3:
        if st.button("Features", key="nav_feat", use_container_width=True, type="secondary" if active_page != "Features" else "primary"):
            st.session_state.active_page = "Features"
            st.rerun()

    with nav_col4:
        if st.button("Practice & Learn", key="nav_practice", use_container_width=True, type="primary" if is_practice_active else "secondary"):
            st.session_state.active_page = "Live App"
            st.session_state.live_mode_view = "Interactive Practice Mode"
            st.session_state["live_mode_selector"] = "Interactive Practice Mode"
            st.rerun()

    with nav_col5:
        if st.button("Studio", key="nav_studio", use_container_width=True, type="secondary" if active_page != "Studio" else "primary"):
            st.session_state.active_page = "Studio"
            st.rerun()

    with nav_col6:
        if st.button("About", key="nav_about", use_container_width=True, type="secondary" if active_page != "About" else "primary"):
            st.session_state.active_page = "About"
            st.rerun()

    with nav_col7:
        if st.button("Start Recognition ↗", key="nav_launch", use_container_width=True, type="primary" if is_live_active else "secondary"):
            st.session_state.active_page = "Live App"
            st.session_state.live_mode_view = "Live Recognition"
            st.session_state["live_mode_selector"] = "Live Recognition"
            st.rerun()

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
