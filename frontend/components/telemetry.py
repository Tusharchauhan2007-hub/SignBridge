"""
Telemetry displays, status badges, and positioning guidance for SignBridge.
Modern dark-tech card layout with reticle icon and monospace spatial parameters.
"""

import streamlit as st


def render_positioning_tips() -> None:
    """Renders the hand positioning guidance card."""
    st.markdown(
        """
        <div style="background:rgba(8, 11, 20, 0.75); border:1px solid var(--sb-border); border-radius:10px; padding:0.85rem 1rem; margin-top:0.75rem;">
            <div style="font-family:'JetBrains Mono', monospace; font-size:0.74rem; font-weight:700; color:#818cf8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.4rem; display:flex; align-items:center; gap:0.4rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                // OPTICAL POSITIONING TELEMETRY
            </div>
            <ul style="margin:0; padding-left:1.15rem; font-size:0.82rem; color:var(--sb-text-muted); line-height:1.55;">
                <li>Keep hand centered inside the sensor viewport at <strong>1.5–3.0 ft (45–90 cm)</strong> distance.</li>
                <li>Ensure uniform frontal illumination without strong backlighting or hand occlusion.</li>
                <li>Hold hand posture steady for <strong>1.0 second</strong> for automatic fingerspelling debounce.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
