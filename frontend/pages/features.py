"""
Features page for SignBridge.
Details core accessibility tech capabilities and features.
Modern dark-tech card layout with monospace indicators, electric indigo and cyan accents.
"""

import streamlit as st


def render_features_page() -> None:
    """Renders the Features overview page with Dark Tech styling."""
    st.markdown(
        """
        <div class="sb-section-tag">// PRODUCT CAPABILITIES & SPECIFICATIONS</div>
        <h1 class="sb-section-heading">Designed for Everyday Accessibility</h1>
        <p class="sb-section-desc">
            Thoughtfully built to empower individuals who use sign language with immediate, natural communication tools.
        </p>
        """,
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns(3, gap="medium")
    with f1:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">// VISION SENSOR</div>
                <div class="sb-step-title">Real-Time Hand Tracking</div>
                <div class="sb-step-text">
                    Continuous 30 FPS skeleton tracking with visual feedback, wrist references, and finger-joint indicators.
                </div>
                <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#06b6d4;">
                    ● 21 3D LANDMARK TOPOLOGY
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">// ALPHABET MATRIX</div>
                <div class="sb-step-title">A–Z Fingerspelling</div>
                <div class="sb-step-text">
                    Support for individual letters allowing signers to spell out names, locations, and specific words naturally.
                </div>
                <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#818cf8;">
                    ● 26 MANUAL ALPHABET CHARACTERS
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">// BUFFER SYNTAX</div>
                <div class="sb-step-title">Sentence Assembly</div>
                <div class="sb-step-text">
                    Letters automatically merge into complete words, while spaces and word signs maintain clean punctuation.
                </div>
                <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#10b981;">
                    ● TEMPORAL DEBOUNCED TOKENIZER
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    f4, f5, f6 = st.columns(3, gap="medium")
    with f4:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">// VOCAL ENGINE</div>
                <div class="sb-step-title">Dual Speech Synthesis</div>
                <div class="sb-step-text">
                    Universal voice output using both native backend audio (pyttsx3) and browser-native HTML5 Web Speech.
                </div>
                <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#818cf8;">
                    ● PYTTSX3 SAPI + HTML5 WEB SPEECH
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f5:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">// STUDIO LAB</div>
                <div class="sb-step-title">In-App Dataset Collector</div>
                <div class="sb-step-text">
                    Capture authentic training samples with session metadata, participant IDs, burst recording, and class balance tracking.
                </div>
                <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#06b6d4;">
                    ● LOCAL CSV DATASET + MODEL TRAINER
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f6:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">// SAFETY GATE</div>
                <div class="sb-step-title">Confidence Gating & Macros</div>
                <div class="sb-step-text">
                    Refuses to invent false predictions when lighting is poor, while supporting custom macros for emergency shortcuts.
                </div>
                <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#10b981;">
                    ● STRICT GATING + MACRO AUTOMATION
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
