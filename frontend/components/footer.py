"""
Footer component for SignBridge with creator credits and brand metadata.
"""

import streamlit as st


def render_footer() -> None:
    """Renders the global accessible footer with credits for Tushar Chauhan & Ujjwal Dhiman."""
    st.markdown(
        """
        <div class="sb-footer">
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:1.5rem; margin-bottom:1.5rem;">
                <div style="max-width:320px;">
                    <div class="sb-footer-brand">SignBridge</div>
                    <div class="sb-footer-text">Communication without barriers. Assistive AI sign language recognition built for accessible everyday communication.</div>
                </div>
                <div>
                    <div class="sb-footer-col-title">Navigation</div>
                    <div class="sb-footer-text">Home • How It Works • Features • Live Recognition • Studio • About</div>
                </div>
                <div>
                    <div class="sb-footer-col-title">Linguistic Scope</div>
                    <div class="sb-footer-text">Indian Sign Language (ISL) • Manual Alphabet (A–Z) • Single-Hand Fingerspelling</div>
                </div>
                <div>
                    <div class="sb-footer-col-title">Privacy & Safety</div>
                    <div class="sb-footer-text">Client-Side Execution • No Cloud Storage • Confidence Gated • Offline Translation</div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem; border-top:1px solid var(--sb-border); padding-top:1.2rem; font-size:0.8rem; color:var(--sb-text-subtle);">
                <div>© 2026 SignBridge. Developed for accessible assistive technology.</div>
                <div style="font-weight:500; color:var(--sb-text-muted);">
                    Made with care by <span style="color:var(--sb-text-main); font-weight:600;">Tushar Chauhan</span> & <span style="color:var(--sb-text-main); font-weight:600;">Ujjwal Dhiman</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

