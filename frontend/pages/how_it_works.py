"""
How It Works page for SignBridge.
Explains the 3-step edge computer vision, normalization, and debounced ML pipeline.
Modern dark-tech card layout with glassmorphic depth, geometric indicators, and pipeline diagram.
"""

import streamlit as st


def render_how_it_works_page() -> None:
    """Renders the How It Works educational page with Dark Tech styling."""
    st.markdown(
        """
        <div class="sb-section-tag">// SYSTEM ARCHITECTURE & PIPELINE</div>
        <h1 class="sb-section-heading">How SignBridge Works</h1>
        <p class="sb-section-desc">
            A comprehensive, privacy-first computer vision and machine learning pipeline
            tailored for accessible communication and edge processing.
        </p>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">// STEP 01: CAPTURE</div>
                <div class="sb-step-title">Hand Landmark Detection</div>
                <div class="sb-step-text">
                    Using Google MediaPipe Tasks API, the system detects 21 hand landmarks
                    per frame with sub-millimeter normalized precision (x, y, z coordinates).
                    Frames are mirrored for an intuitive signer experience.
                </div>
                <div style="margin-top:1.25rem; padding-top:0.75rem; border-top:1px solid rgba(255,255,255,0.06); font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#06b6d4;">
                    ● 21 3D COORDINATES (63 RAW DIMS)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">// STEP 02: NORMALIZE</div>
                <div class="sb-step-title">Geometric Invariance</div>
                <div class="sb-step-text">
                    Raw coordinates are transformed relative to the wrist (landmark 0) and scaled
                    by the distance to the middle finger knuckle. This makes recognition invariant
                    to camera distance, framing, signer position, or hand scale.
                </div>
                <div style="margin-top:1.25rem; padding-top:0.75rem; border-top:1px solid rgba(255,255,255,0.06); font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#818cf8;">
                    ● TRANSLATION & SCALE INVARIANT
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">// STEP 03: STABILIZE</div>
                <div class="sb-step-title">Window Debouncing & Speech</div>
                <div class="sb-step-text">
                    A rolling 7-frame majority voting buffer eliminates video flicker.
                    Recognized letters assemble into full words, while temporal debouncing
                    prevents identical characters from repeating unintentionally.
                </div>
                <div style="margin-top:1.25rem; padding-top:0.75rem; border-top:1px solid rgba(255,255,255,0.06); font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#10b981;">
                    ● 7-FRAME ROLLING MAJORITY BUFFER
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # Machine Learning Architecture Callout
    st.markdown(
        """
        <div class="sb-callout" style="padding: 1.75rem;">
            <div class="sb-callout-title" style="font-size: 1.2rem; margin-bottom: 0.6rem;">
                <span class="sb-status-dot sb-dot-active"></span>
                <span>Machine Learning Architecture & Responsible Edge Evaluation</span>
            </div>
            <div class="sb-callout-text" style="font-size: 0.92rem; line-height: 1.65;">
                SignBridge uses a Random Forest Classifier with balanced class weighting. Unlike black-box neural networks,
                geometric Random Forests evaluate joint angles directly, run at over 60 FPS on standard CPUs,
                and prevent data leakage using session-based cross-validation (<code>GroupShuffleSplit</code>).
            </div>
            <div style="margin-top:1rem; display:flex; gap:0.75rem; flex-wrap:wrap;">
                <span class="sb-status-chip"><span class="sb-status-dot sb-dot-ready"></span>ZERO CLOUD LATENCY</span>
                <span class="sb-status-chip"><span class="sb-status-dot sb-dot-cyan"></span>CPU INFERENCE &lt; 5MS</span>
                <span class="sb-status-chip"><span class="sb-status-dot sb-dot-pass"></span>GROUPSHUFFLESPLIT VALIDATED</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
