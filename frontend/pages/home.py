"""
Landing page (Home) for SignBridge.
Renders hero section, product preview mockup, 3-step methodology, feature highlights,
vocabulary coverage grid, and creator credits.
"""

import streamlit as st
from backend.data_collection import DatasetManager, CORE_ISL_GESTURES, ISL_ALPHABET_LETTERS
from backend.predictor import SignPredictor


def render_home_page(dataset_mgr: DatasetManager, predictor: SignPredictor) -> None:
    """Renders the complete landing page for SignBridge."""
    # Hero Section: Two-Column Editorial Layout
    col_hero_text, col_hero_mock = st.columns([1.15, 0.85], gap="large")

    with col_hero_text:
        st.markdown(
            """
            <div class="sb-hero-tag">Assistive Computer Vision • Edge AI</div>
            <h1 class="sb-hero-title">Communication<br>without barriers.</h1>
            <p class="sb-hero-sub">
                A modern accessibility platform translating Indian Sign Language and manual fingerspelling
                into clear text and speech directly on your local device.
            </p>
            """,
            unsafe_allow_html=True,
        )

        c_cta1, c_cta2 = st.columns([1.15, 1.1])
        with c_cta1:
            if st.button("Launch SignBridge →", type="primary", use_container_width=True, key="hero_primary"):
                st.session_state.active_page = "Live App"
                st.rerun()
        with c_cta2:
            if st.button("Explore How It Works", use_container_width=True, key="hero_secondary"):
                st.session_state.active_page = "How It Works"
                st.rerun()

        st.markdown(
            """
            <div class="sb-hero-notice">
                <strong>Responsible AI Transparency:</strong> Focuses on static ISL gestures and A–Z manual alphabet fingerspelling.
                Designed as a real-time accessibility assistant without cloud video transmission.
            </div>
            <div style="margin-top: 1.15rem; display: inline-flex; align-items: center; gap: 0.5rem; font-size: 0.82rem; color: var(--sb-text-muted); padding: 0.35rem 0.8rem; background: var(--sb-surface); border: 1px solid var(--sb-border); border-radius: 999px; box-shadow: var(--sb-shadow);">
                <span style="color: var(--sb-primary); font-size: 0.72rem;">●</span>
                <span>A project by <strong style="color: var(--sb-text-main); font-weight: 600;">Tushar Chauhan</strong> and <strong style="color: var(--sb-text-main); font-weight: 600;">Ujjwal Dhiman</strong></span>
            </div>
            <div style="margin-top: 0.45rem; font-size: 0.76rem; color: var(--sb-text-subtle);">
                Made by Tushar Chauhan and Ujjwal Dhiman
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_hero_mock:
        # High-Fidelity Product Preview Mockup Window
        st.markdown(
            """
            <div class="sb-preview-window">
                <div class="sb-preview-header">
                    <div class="sb-preview-dots">
                        <div class="sb-dot"></div>
                        <div class="sb-dot"></div>
                        <div class="sb-dot"></div>
                    </div>
                    <span>SignBridge • Live Session</span>
                    <span style="color: var(--sb-success); font-weight: 600;">● 30 FPS • Local</span>
                </div>
                <div class="sb-preview-body">
                    <div class="sb-preview-screen">
                        <div class="sb-preview-overlay">MediaPipe 3D HandLandmarker</div>
                        <svg width="130" height="135" viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <!-- Hand palm & wrist base lines -->
                            <line x1="50" y1="102" x2="34" y2="76" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="50" y1="102" x2="43" y2="66" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="50" y1="102" x2="53" y2="65" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="50" y1="102" x2="63" y2="69" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="50" y1="102" x2="73" y2="76" stroke="#818cf8" stroke-width="1.8"/>
                            <!-- Knuckle interconnects -->
                            <line x1="34" y1="76" x2="43" y2="66" stroke="#6366f1" stroke-width="1.2" stroke-dasharray="2 2"/>
                            <line x1="43" y1="66" x2="53" y2="65" stroke="#6366f1" stroke-width="1.2" stroke-dasharray="2 2"/>
                            <line x1="53" y1="65" x2="63" y2="69" stroke="#6366f1" stroke-width="1.2" stroke-dasharray="2 2"/>
                            <line x1="63" y1="69" x2="73" y2="76" stroke="#6366f1" stroke-width="1.2" stroke-dasharray="2 2"/>
                            <!-- Phalanges / Fingers -->
                            <line x1="34" y1="76" x2="24" y2="58" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="24" y1="58" x2="18" y2="46" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="43" y1="66" x2="40" y2="46" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="40" y1="46" x2="38" y2="30" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="53" y1="65" x2="53" y2="43" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="53" y1="43" x2="53" y2="25" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="63" y1="69" x2="65" y2="48" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="65" y1="48" x2="67" y2="33" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="73" y1="76" x2="77" y2="60" stroke="#818cf8" stroke-width="1.8"/>
                            <line x1="77" y1="60" x2="81" y2="48" stroke="#818cf8" stroke-width="1.8"/>
                            <!-- Spatial Joints -->
                            <circle cx="50" cy="102" r="3.5" fill="#4338ca" stroke="#c7d2fe" stroke-width="1"/>
                            <circle cx="34" cy="76" r="2.5" fill="#6366f1"/>
                            <circle cx="24" cy="58" r="2.5" fill="#6366f1"/>
                            <circle cx="18" cy="46" r="3" fill="#38bdf8"/>
                            <circle cx="43" cy="66" r="2.5" fill="#6366f1"/>
                            <circle cx="40" cy="46" r="2.5" fill="#6366f1"/>
                            <circle cx="38" cy="30" r="3" fill="#38bdf8"/>
                            <circle cx="53" cy="65" r="2.5" fill="#6366f1"/>
                            <circle cx="53" cy="43" r="2.5" fill="#6366f1"/>
                            <circle cx="53" cy="25" r="3" fill="#38bdf8"/>
                            <circle cx="63" cy="69" r="2.5" fill="#6366f1"/>
                            <circle cx="65" cy="48" r="2.5" fill="#6366f1"/>
                            <circle cx="67" cy="33" r="3" fill="#38bdf8"/>
                            <circle cx="73" cy="76" r="2.5" fill="#6366f1"/>
                            <circle cx="77" cy="60" r="2.5" fill="#6366f1"/>
                            <circle cx="81" cy="48" r="3" fill="#38bdf8"/>
                        </svg>
                        <div class="sb-preview-pill">YES • 96% CONFIDENCE</div>
                    </div>
                    <div style="font-size: 0.72rem; color: var(--sb-text-subtle); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.85rem; font-weight: 600;">
                        Assembled Output
                    </div>
                    <div class="sb-preview-footer">
                        HELLO YES <span style="color: var(--sb-primary); font-weight: 700;">|</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    # 3-Step Methodology Section
    st.markdown(
        """
        <div class="sb-section-tag">Methodology</div>
        <h2 class="sb-section-heading">How SignBridge Works</h2>
        <p class="sb-section-desc">
            A three-step edge machine learning pipeline that preserves privacy and operates entirely on your local machine.
        </p>
        """,
        unsafe_allow_html=True,
    )

    c_step1, c_step2, c_step3 = st.columns(3, gap="medium")
    with c_step1:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">STEP 01</div>
                <div class="sb-step-title">Capture Hand Landmarks</div>
                <div class="sb-step-text">
                    MediaPipe Tasks HandLandmarker tracks 21 spatial joints in real time directly from standard webcam frames.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_step2:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">STEP 02</div>
                <div class="sb-step-title">Normalize & Classify</div>
                <div class="sb-step-text">
                    Hand coordinates are normalized relative to wrist translation and hand scale into 63 invariant geometric features.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_step3:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">STEP 03</div>
                <div class="sb-step-title">Build Text & Vocalize</div>
                <div class="sb-step-text">
                    A temporal debouncing engine filters jitter, concatenates fingerspelled words, and speaks using dual TTS synthesis.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    # Feature Highlights Section
    st.markdown(
        """
        <div class="sb-section-tag">Core Features</div>
        <h2 class="sb-section-heading">Assistive Intelligence by Design</h2>
        <p class="sb-section-desc">
            Engineered with accessibility-first principles to bridge everyday communication effortlessly.
        </p>
        """,
        unsafe_allow_html=True,
    )

    h_col1, h_col2, h_col3, h_col4 = st.columns(4, gap="medium")
    with h_col1:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">RECOGNITION</div>
                <div class="sb-step-title">A–Z Fingerspelling</div>
                <div class="sb-step-text">
                    Complete manual alphabet recognition supporting letters, custom signs, and core ISL gestures.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with h_col2:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">COMPOSITION</div>
                <div class="sb-step-title">Smart Sentence Assembly</div>
                <div class="sb-step-text">
                    Automatic character concatenation with single-character backspace, spaces, and duplicate suppression.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with h_col3:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">VOCALIZATION</div>
                <div class="sb-step-title">Dual Speech Output</div>
                <div class="sb-step-text">
                    Instant voice output combining offline Python pyttsx3 with browser-native HTML5 Web Speech.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with h_col4:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">TRANSLATION</div>
                <div class="sb-step-title">Offline Hindi Translation</div>
                <div class="sb-step-text">
                    One-click neural English-to-Hindi translation using MarianMT seq2seq transformer without any cloud APIs.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    # Supported Vocabulary Section
    st.markdown(
        """
        <div class="sb-section-tag">Vocabulary & Linguistic Coverage</div>
        <h2 class="sb-section-heading">Supported Signs & Fingerspelling</h2>
        <p class="sb-section-desc">
            SignBridge supports core Indian Sign Language gestures and the full manual alphabet space (A–Z).
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_voc1, col_voc2 = st.columns([1, 1], gap="large")
    with col_voc1:
        st.markdown("#### Active Model Vocabulary")
        if predictor.is_loaded:
            active_gestures = [s for s in predictor.classes if s in CORE_ISL_GESTURES]
            active_letters = [s for s in predictor.classes if s in ISL_ALPHABET_LETTERS]
            other_signs = [s for s in predictor.classes if s not in CORE_ISL_GESTURES and s not in ISL_ALPHABET_LETTERS]

            st.write(f"The active model currently recognizes **{len(predictor.classes)}** distinct classes:")
            if active_gestures:
                st.markdown("**Core Word Signs:** " + " ".join([f"`{g}`" for g in active_gestures]))
            if active_letters:
                st.markdown("**Alphabet Letters:** " + " ".join([f"`{l}`" for l in active_letters]))
            if other_signs:
                st.markdown("**Custom Signs:** " + " ".join([f"`{o}`" for o in other_signs]))
        else:
            st.info("No active model artifact loaded.")

        st.markdown(
            """
            <div class="sb-callout" style="margin-top: 1.5rem;">
                <div class="sb-callout-title">
                    Linguistic Grounding: ISL vs. ASL
                </div>
                <div class="sb-callout-text">
                    Standard Indian Sign Language (codified by ISLRTC) historically uses a <em>two-handed</em> manual alphabet.
                    Single-handed adaptations are used in single-camera vision systems.
                    SignBridge strictly differentiates between ISL fingerspelling conventions and American Sign Language (ASL).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_voc2:
        st.markdown("#### Alphabet Coverage Status (A–Z)")
        st.caption("Real-time dataset and model readiness for manual alphabet letters (A–Z):")

        cov_items = dataset_mgr.get_alphabet_coverage_status(predictor.classes if predictor.is_loaded else [])
        
        # 6-column clean matrix
        cols_alpha = st.columns(6)
        for idx, item in enumerate(cov_items):
            c = cols_alpha[idx % 6]
            let = item["letter"]
            cnt = item["count"]
            code = item["status_code"]
            
            if code == "ACTIVE":
                badge_class = "sb-matrix-badge-active"
                label_txt = "Active"
            elif code == "READY":
                badge_class = "sb-matrix-badge-ready"
                label_txt = f"Ready ({cnt})"
            else:
                badge_class = "sb-matrix-badge-needs"
                label_txt = "Needs data"

            c.markdown(
                f"<div class='sb-matrix-cell'>"
                f"<div class='sb-matrix-letter'>{let}</div>"
                f"<span class='{badge_class}'>{label_txt}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="font-size:0.75rem; color:var(--sb-text-subtle); margin-top:0.6rem; line-height:1.4;">
                <span style="color:var(--sb-success); font-weight:600;">● Active in classifier</span>: Included in active trained model.<br>
                <span style="color:var(--sb-warning); font-weight:600;">▲ Ready to train</span>: Samples exist in dataset, awaiting retraining.<br>
                <span style="color:var(--sb-text-subtle); font-weight:600;">○ Needs data</span>: 0 samples recorded yet.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
        # Quick letter selection to jump straight to recording
        sel_col1, sel_col2 = st.columns([1.5, 1.5])
        with sel_col1:
            cov_labels = [f"{it['letter']} — {it['status']} ({it['count']} samples)" for it in cov_items]
            selected_cov_idx = st.selectbox(
                "Select letter to collect:",
                range(len(cov_items)),
                format_func=lambda i: cov_labels[i],
                key="home_letter_sel",
            )
            chosen_letter = cov_items[selected_cov_idx]["letter"]
        with sel_col2:
            st.markdown("<div style='height: 1.7rem;'></div>", unsafe_allow_html=True)
            if st.button(f"Collect '{chosen_letter}' in Studio →", type="primary", use_container_width=True, key="home_go_studio_btn"):
                st.session_state.target_letter = chosen_letter
                st.session_state.target_category = "Alphabet Letters (A–Z)"
                st.session_state.active_page = "Studio"
                st.rerun()

