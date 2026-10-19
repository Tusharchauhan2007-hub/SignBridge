"""
Telemetry displays, status badges, and positioning guidance for SignBridge.
"""

import streamlit as st


def render_positioning_tips() -> None:
    """Renders the hand positioning guidance card."""
    st.markdown(
        """
        <div style="background:var(--sb-surface-muted); border:1px solid var(--sb-border); border-radius:6px; padding:0.75rem 0.9rem; margin-top:0.75rem;">
            <div style="font-size:0.75rem; font-weight:700; color:var(--sb-text-main); margin-bottom:0.35rem; display:flex; align-items:center; gap:0.4rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                Hand Positioning Guidance
            </div>
            <ul style="margin:0; padding-left:1.15rem; font-size:0.78rem; color:var(--sb-text-muted); line-height:1.45;">
                <li>Keep hand centered and <strong>1.5–3 feet</strong> from the lens.</li>
                <li>Maintain good frontal lighting without harsh shadows.</li>
                <li>Hold steady for <strong>1 second</strong> for automatic fingerspelling.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

