"""
Footer component for SignBridge with creator credits, repository link, and brand metadata.
Sophisticated dark-tech layout with clean columns, glassmorphic styling, and monospace status indicators.
"""

import streamlit as st


def render_footer() -> None:
    """Renders the global accessible footer with credits for Tushar Chauhan & Ujjwal Dhiman."""
    st.markdown(
        """
        <div class="sb-footer">
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:2rem; margin-bottom:2rem;">
                <div style="max-width:320px;">
                    <div class="sb-footer-brand">SignBridge</div>
                    <div class="sb-footer-text">
                        Bridging signs and connecting voices. High-performance assistive computer vision and offline neural translation engineered for accessible everyday communication.
                    </div>
                    <div style="margin-top:0.85rem;">
                        <a href="https://github.com/Tusharchauhan2007-hub/SignBridge.git" target="_blank" style="text-decoration:none; display:inline-flex; align-items:center; gap:6px; font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#818cf8; border:1px solid rgba(99,102,241,0.25); border-radius:6px; padding:6px 12px; background:rgba(99,102,241,0.1);">
                            <span>GITHUB // REPOSITORY ↗</span>
                        </a>
                    </div>
                </div>
                <div>
                    <div class="sb-footer-col-title">// Navigation</div>
                    <div class="sb-footer-text" style="font-family:'JetBrains Mono', monospace; font-size:0.78rem; line-height:1.8;">
                        • Home<br>
                        • How It Works<br>
                        • Features<br>
                        • Live Recognition<br>
                        • Practice & Learn<br>
                        • Studio (Dataset Manager)<br>
                        • About & Ethics
                    </div>
                </div>
                <div>
                    <div class="sb-footer-col-title">// Linguistic Scope</div>
                    <div class="sb-footer-text" style="line-height:1.7;">
                        • Indian Sign Language (ISL)<br>
                        • Manual Alphabet (A–Z)<br>
                        • Single-Hand Fingerspelling<br>
                        • 5 Core Words (HELLO, YES, NO, THANK YOU, HELP)
                    </div>
                </div>
                <div>
                    <div class="sb-footer-col-title">// Privacy & Architecture</div>
                    <div class="sb-footer-text" style="line-height:1.7;">
                        • Client-Side Vision (OpenCV & MediaPipe)<br>
                        • Offline Neural Translation (MarianMT)<br>
                        • Zero Cloud Video Transmission<br>
                        • Hard Resource Budget Enforced
                    </div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; border-top:1px solid rgba(99, 102, 241, 0.22); padding-top:1.5rem; font-size:0.8rem; color:#94a3b8;">
                <div style="font-family:'JetBrains Mono', monospace; font-size:0.74rem;">
                    © 2026 SignBridge // ACCESSIBLE ASSISTIVE TECHNOLOGY
                </div>
                <div style="font-size:0.84rem; color:var(--sb-text-muted);">
                    Made with care by <strong style="color: var(--sb-text-main); font-weight: 600;">Tushar Chauhan</strong> & <strong style="color: var(--sb-text-main); font-weight: 600;">Ujjwal Dhiman</strong>
                </div>
            </div>
            <div style="margin-top:0.4rem; font-size:0.74rem; color:#64748b; font-family:'JetBrains Mono', monospace;">
                A project by Tushar Chauhan and Ujjwal Dhiman
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
