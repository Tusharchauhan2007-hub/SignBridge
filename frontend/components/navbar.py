"""
Navigation bar and theme toggle component for SignBridge.
"""

import streamlit as st


def _toggle_theme():
    """Toggles between light and dark theme mode and persists in query params."""
    curr = st.session_state.get("theme", "light")
    nxt = "dark" if curr == "light" else "light"
    st.session_state.theme = nxt
    try:
        st.query_params["theme"] = nxt
    except Exception:
        pass


def render_navbar() -> None:
    """Renders the top branding bar, theme toggle, and page navigation buttons."""
    nav_top_col, nav_theme_col = st.columns([4.2, 1.2])
    with nav_top_col:
        st.markdown(
            """
            <div class="sb-navbar" style="margin-bottom:0;">
                <div class="sb-brand">
                    <div class="sb-brand-logo">S</div>
                    <span class="sb-brand-name">SignBridge</span>
                    <span class="sb-brand-badge">Accessible AI</span>
                </div>
                <div class="sb-nav-tagline">
                    Communication without barriers
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with nav_theme_col:
        is_dark = st.session_state.theme == "dark"
        theme_btn_label = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
        st.button(
            theme_btn_label,
            key="theme_toggle_btn",
            use_container_width=True,
            on_click=_toggle_theme,
        )

    # Navigation Menu Buttons (Production Tabs Style)
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns([1, 1, 1, 1, 1, 1.2])

    with nav_col1:
        if st.button("Home", key="nav_home", use_container_width=True, type="secondary" if st.session_state.active_page != "Home" else "primary"):
            st.session_state.active_page = "Home"
            st.rerun()

    with nav_col2:
        if st.button("How It Works", key="nav_how", use_container_width=True, type="secondary" if st.session_state.active_page != "How It Works" else "primary"):
            st.session_state.active_page = "How It Works"
            st.rerun()

    with nav_col3:
        if st.button("Features", key="nav_feat", use_container_width=True, type="secondary" if st.session_state.active_page != "Features" else "primary"):
            st.session_state.active_page = "Features"
            st.rerun()

    with nav_col4:
        if st.button("Studio", key="nav_studio", use_container_width=True, type="secondary" if st.session_state.active_page != "Studio" else "primary"):
            st.session_state.active_page = "Studio"
            st.rerun()

    with nav_col5:
        if st.button("About", key="nav_about", use_container_width=True, type="secondary" if st.session_state.active_page != "About" else "primary"):
            st.session_state.active_page = "About"
            st.rerun()

    with nav_col6:
        if st.button("Launch App", key="nav_launch", use_container_width=True, type="primary" if st.session_state.active_page == "Live App" else "secondary"):
            st.session_state.active_page = "Live App"
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Release webcam device if navigating away from Live App
    if st.session_state.active_page != "Live App" and st.session_state.get("live_webcam_cap") is not None:
        try:
            st.session_state.live_webcam_cap.release()
        except Exception:
            pass
        st.session_state.live_webcam_cap = None
