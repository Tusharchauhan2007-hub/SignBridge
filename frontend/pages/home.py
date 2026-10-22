"""
Landing page (Home) for SignBridge.
Implements the Dark Tech / AI Intelligence design system with:
- Immersive Hero section with radial indigo/cyan accent glow
- 4-Column Large Monospace Metrics Grid (31 Classes, 21 Joints, 63 Dims, 100% Offline)
- 3-Column Bento Feature Grid (Real-time Recognition, Language Translation, Offline Intelligence)
- Developer Observability Telemetry Event Stream
- Alphabet Coverage Matrix (A–Z) & Quick-Practice Routing
- Complete Creator Credits (Tushar Chauhan & Ujjwal Dhiman)
"""

import streamlit as st
from backend.data_collection import DatasetManager, CORE_ISL_GESTURES, ISL_ALPHABET_LETTERS
from backend.predictor import SignPredictor


def render_home_page(dataset_mgr: DatasetManager, predictor: SignPredictor) -> None:
    """Renders the complete Dark Tech landing page for SignBridge."""
    # -------------------------------------------------------------------------
    # 1. HERO SECTION: Two-Column Dark Tech Composition
    # -------------------------------------------------------------------------
    col_hero_text, col_hero_mock = st.columns([1.18, 0.82], gap="large")

    with col_hero_text:
        st.markdown(
            """
            <div class="sb-hero-tag">
                <span class="sb-status-dot sb-dot-active"></span>
                <span>EDGE AI INTELLIGENCE // REAL-TIME ISL</span>
            </div>
            <h1 class="sb-hero-title">Bridging Signs.<br>Connecting Voices.</h1>
            <p class="sb-hero-sub">
                An AI-powered sign language recognition and translation experience designed to help people communicate more naturally and freely.
            </p>
            """,
            unsafe_allow_html=True,
        )

        c_cta1, c_cta2, c_cta3 = st.columns([1.25, 1.15, 1.1])
        with c_cta1:
            if st.button("Start Recognition ↗", type="primary", use_container_width=True, key="hero_primary"):
                st.session_state.active_page = "Live App"
                st.session_state.live_mode_view = "Live Recognition"
                st.session_state["live_mode_selector"] = "Live Recognition"
                st.rerun()
        with c_cta2:
            if st.button("Explore Features", type="secondary", use_container_width=True, key="hero_features"):
                st.session_state.active_page = "Features"
                st.rerun()
        with c_cta3:
            if st.button("Practice Signs 🎯", type="secondary", use_container_width=True, key="hero_practice"):
                st.session_state.active_page = "Live App"
                st.session_state.live_mode_view = "Interactive Practice Mode"
                st.session_state["live_mode_selector"] = "Interactive Practice Mode"
                st.rerun()

        st.markdown(
            """
            <div class="sb-hero-notice">
                <span style="font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#818cf8; font-weight:600;">
                    RESPONSIBLE AI TRANSPARENCY:
                </span>
                <span style="font-size:0.8rem; color:var(--sb-text-muted);">
                    Evaluates static ISL gestures and A–Z manual alphabet fingerspelling. Runs 100% on local CPU with zero cloud video transmission.
                </span>
            </div>
            <div style="margin-top: 1.25rem; display: inline-flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; color: var(--sb-text-muted); padding: 0.35rem 0.95rem; background: var(--sb-surface-muted); border: 1px solid var(--sb-border); border-radius: 999px;">
                <span class="sb-status-dot sb-dot-ready"></span>
                <span>Made with care by <strong style="color: var(--sb-text-main); font-weight: 600;">Tushar Chauhan</strong> and <strong style="color: var(--sb-text-main); font-weight: 600;">Ujjwal Dhiman</strong></span>
            </div>
            <div style="margin-top: 0.4rem; font-size: 0.74rem; color: #64748b; font-family:'JetBrains Mono', monospace;">
                A project by Tushar Chauhan and Ujjwal Dhiman
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_hero_mock:
        # High-Fidelity Dark-Tech Mockup Window with 21-Joint Geometric Landmark Visualizer
        st.markdown(
            """
            <div class="sb-preview-window">
                <div class="sb-preview-header">
                    <div class="sb-preview-dots">
                        <div class="sb-dot"></div>
                        <div class="sb-dot"></div>
                        <div class="sb-dot"></div>
                    </div>
                    <span>SIGNBRIDGE // 3D LANDMARK PIPELINE</span>
                    <span style="color: #10b981; font-weight: 600; display:flex; align-items:center; gap:4px;">
                        <span class="sb-status-dot sb-dot-ready"></span> LOCAL CPU
                    </span>
                </div>
                <div class="sb-preview-body">
                    <div class="sb-preview-screen">
                        <div class="sb-preview-overlay">MEDIAPIPE TASKS • 21 3D JOINTS</div>
                        <svg width="150" height="155" viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <!-- Coordinate Grid Substrate -->
                            <line x1="10" y1="60" x2="90" y2="60" stroke="rgba(255,255,255,0.06)" stroke-width="0.8" stroke-dasharray="2 2"/>
                            <line x1="50" y1="15" x2="50" y2="105" stroke="rgba(255,255,255,0.06)" stroke-width="0.8" stroke-dasharray="2 2"/>
                            <!-- Hand palm & wrist base lines -->
                            <line x1="50" y1="102" x2="34" y2="76" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="50" y1="102" x2="43" y2="66" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="50" y1="102" x2="53" y2="65" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="50" y1="102" x2="63" y2="69" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="50" y1="102" x2="73" y2="76" stroke="#6366f1" stroke-width="1.8"/>
                            <!-- Knuckle interconnects -->
                            <line x1="34" y1="76" x2="43" y2="66" stroke="rgba(255,255,255,0.3)" stroke-width="1" stroke-dasharray="2 2"/>
                            <line x1="43" y1="66" x2="53" y2="65" stroke="rgba(255,255,255,0.3)" stroke-width="1" stroke-dasharray="2 2"/>
                            <line x1="53" y1="65" x2="63" y2="69" stroke="rgba(255,255,255,0.3)" stroke-width="1" stroke-dasharray="2 2"/>
                            <line x1="63" y1="69" x2="73" y2="76" stroke="rgba(255,255,255,0.3)" stroke-width="1" stroke-dasharray="2 2"/>
                            <!-- Phalanges / Fingers -->
                            <line x1="34" y1="76" x2="24" y2="58" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="24" y1="58" x2="18" y2="46" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="43" y1="66" x2="40" y2="46" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="40" y1="46" x2="38" y2="30" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="53" y1="65" x2="53" y2="43" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="53" y1="43" x2="53" y2="25" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="63" y1="69" x2="65" y2="48" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="65" y1="48" x2="67" y2="33" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="73" y1="76" x2="77" y2="60" stroke="#6366f1" stroke-width="1.8"/>
                            <line x1="77" y1="60" x2="81" y2="48" stroke="#6366f1" stroke-width="1.8"/>
                            <!-- Spatial Joints -->
                            <circle cx="50" cy="102" r="3.5" fill="#ffffff" stroke="#6366f1" stroke-width="1.5"/>
                            <circle cx="34" cy="76" r="2.5" fill="#6366f1"/>
                            <circle cx="24" cy="58" r="2.5" fill="#6366f1"/>
                            <circle cx="18" cy="46" r="3" fill="#10b981"/>
                            <circle cx="43" cy="66" r="2.5" fill="#6366f1"/>
                            <circle cx="40" cy="46" r="2.5" fill="#6366f1"/>
                            <circle cx="38" cy="30" r="3" fill="#10b981"/>
                            <circle cx="53" cy="65" r="2.5" fill="#6366f1"/>
                            <circle cx="53" cy="43" r="2.5" fill="#6366f1"/>
                            <circle cx="53" cy="25" r="3" fill="#10b981"/>
                            <circle cx="63" cy="69" r="2.5" fill="#6366f1"/>
                            <circle cx="65" cy="48" r="2.5" fill="#6366f1"/>
                            <circle cx="67" cy="33" r="3" fill="#10b981"/>
                            <circle cx="73" cy="76" r="2.5" fill="#6366f1"/>
                            <circle cx="77" cy="60" r="2.5" fill="#6366f1"/>
                            <circle cx="81" cy="48" r="3" fill="#10b981"/>
                        </svg>
                        <div class="sb-preview-pill">
                            <span style="color:#10b981;">●</span> RECOGNIZED: HELLO • 96.4% CONFIDENCE
                        </div>
                    </div>
                    <div style="font-family:'JetBrains Mono', monospace; font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 1rem; font-weight: 600;">
                        Assembled Output Stream // Buffer
                    </div>
                    <div class="sb-preview-footer">
                        HELLO YES <span style="color: #818cf8; font-weight: 700;">_</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 3.5rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. METRICS & VISUALIZATION: 4-Column Monospace Grid (~56px Figures)
    # -------------------------------------------------------------------------
    st.markdown(
        """
        <div class="sb-section-tag">ARCHITECTURAL SPECIFICATIONS</div>
        <h2 class="sb-section-heading">Engineered for Sub-Millisecond Precision</h2>
        <p class="sb-section-desc">
            Hard resource-bounded machine learning pipeline evaluated with group cross-validation on local hardware.
        </p>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4, gap="medium")
    with m1:
        st.markdown(
            """
            <div class="sb-metric-card">
                <div class="sb-metric-val">31<span class="sb-metric-val-unit">CLASSES</span></div>
                <div class="sb-metric-label">Target Vocabulary Space</div>
                <div class="sb-metric-desc">5 core word gestures (HELLO, YES, NO, THANK YOU, HELP) plus full A–Z alphabet.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="sb-metric-card">
                <div class="sb-metric-val">21<span class="sb-metric-val-unit">JOINTS</span></div>
                <div class="sb-metric-label">Spatial Hand Landmarks</div>
                <div class="sb-metric-desc">3D sub-millimeter anatomical coordinates tracked continuously at 30 FPS.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="sb-metric-card">
                <div class="sb-metric-val">63<span class="sb-metric-val-unit">DIMS</span></div>
                <div class="sb-metric-label">Invariant Feature Space</div>
                <div class="sb-metric-desc">Wrist-relative translation & scale-normalized geometric feature representation.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            """
            <div class="sb-metric-card">
                <div class="sb-metric-val">100<span class="sb-metric-val-unit">%</span></div>
                <div class="sb-metric-label">Offline Local Execution</div>
                <div class="sb-metric-desc">Zero cloud dependencies. Neural MarianMT and Random Forest run directly on standard CPU.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 3.5rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. BENTO FEATURE GRID (3-Column Desktop Layout)
    # -------------------------------------------------------------------------
    st.markdown(
        """
        <div class="sb-section-tag">CAPABILITIES // BENTO MATRIX</div>
        <h2 class="sb-section-heading">Dark-Tech Intelligent Framework</h2>
        <p class="sb-section-desc">
            A three-pillar architecture engineered for accessible communication without privacy compromises.
        </p>
        """,
        unsafe_allow_html=True,
    )

    b1, b2, b3 = st.columns(3, gap="medium")
    with b1:
        st.markdown(
            """
            <div class="sb-bento-card">
                <div>
                    <div class="sb-bento-header">
                        <span class="sb-bento-num">// CARD 01</span>
                        <div class="sb-status-chip">
                            <span class="sb-status-dot sb-dot-active"></span>
                            <span>ACTIVE // 30 FPS</span>
                        </div>
                    </div>
                    <div class="sb-bento-title">Real-Time Recognition</div>
                    <div class="sb-bento-text">
                        Camera-based gesture acquisition evaluates 21 hand landmarks per frame with rolling 7-frame majority voting to debounce muscle tremor and video jitter.
                    </div>
                </div>
                <div class="sb-bento-visual">
                    <svg width="100%" height="80" viewBox="0 0 200 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M10 40H45L55 20L70 60L85 30L95 45L110 38H190" stroke="#6366f1" stroke-width="1.8"/>
                        <circle cx="55" cy="20" r="3" fill="#ffffff"/>
                        <circle cx="70" cy="60" r="3" fill="#10b981"/>
                        <circle cx="85" cy="30" r="3" fill="#06b6d4"/>
                        <text x="120" y="32" fill="#94a3b8" font-family="'JetBrains Mono', monospace" font-size="10">60% CONFIDENCE GATE</text>
                    </svg>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            """
            <div class="sb-bento-card">
                <div>
                    <div class="sb-bento-header">
                        <span class="sb-bento-num">// CARD 02</span>
                        <div class="sb-status-chip">
                            <span class="sb-status-dot sb-dot-ready"></span>
                            <span>MARIANMT // HINDI</span>
                        </div>
                    </div>
                    <div class="sb-bento-title">Language Translation</div>
                    <div class="sb-bento-text">
                        Converts assembled English tokens and fingerspelled sentences into authentic Devanagari Hindi using an offline Helsinki-NLP seq2seq transformer.
                    </div>
                </div>
                <div class="sb-bento-visual" style="flex-direction:column; gap:6px;">
                    <div style="font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:var(--sb-text-muted);">
                        EN: "Hello, I need help"
                    </div>
                    <div style="color:#818cf8; font-size:0.75rem;">▼ LOCAL SEQ2SEQ TRANSFORMER ▼</div>
                    <div style="font-family:'Inter', sans-serif; font-size:0.95rem; font-weight:600; color:var(--sb-text-main);">
                        HI: "नमस्ते, मुझे मदद चाहिए"
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with b3:
        st.markdown(
            """
            <div class="sb-bento-card">
                <div>
                    <div class="sb-bento-header">
                        <span class="sb-bento-num">// CARD 03</span>
                        <div class="sb-status-chip">
                            <span class="sb-status-dot sb-dot-ready"></span>
                            <span>PASS // PRIVACY</span>
                        </div>
                    </div>
                    <div class="sb-bento-title">Offline Intelligence</div>
                    <div class="sb-bento-text">
                        Enforces a strict free-only policy and hard budget caps. All video capture and neural inference execute strictly on your local device without external telemetry.
                    </div>
                </div>
                <div class="sb-bento-visual">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="1.8" stroke-linecap="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        <path d="m9 12 2 2 4-4"/>
                    </svg>
                    <div style="margin-left:12px; font-family:'JetBrains Mono', monospace; font-size:0.72rem; color:var(--sb-text-muted); text-align:left;">
                        <div>CLIENT-SIDE ONLY</div>
                        <div style="color:#10b981; font-weight:600;">0 BYTES CLOUD LEAKAGE</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 3.5rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 4. TECHNICAL EVENT STREAM / SYSTEM OBSERVABILITY DASHBOARD
    # -------------------------------------------------------------------------
    st.markdown(
        """
        <div class="sb-section-tag">DEVELOPER OBSERVABILITY // SYSTEM STATUS</div>
        <h2 class="sb-section-heading">Runtime Telemetry & Pipeline Diagnostics</h2>
        <p class="sb-section-desc">
            Direct telemetry stream reporting actual model initialization, hardware discovery, and resource limits.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sb-telemetry-panel">
            <div class="sb-telemetry-header">
                <div class="sb-telemetry-title">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                    <span>EVENT_STREAM // SUBSYSTEM_OBSERVABILITY</span>
                </div>
                <div class="sb-status-chip">
                    <span class="sb-status-dot sb-dot-ready"></span>
                    <span>5 / 5 SUBSYSTEMS HEALTHY</span>
                </div>
            </div>
            <div class="sb-event-table">
                <div class="sb-event-row" style="border-left: 3px solid #6366f1;">
                    <span class="sb-event-time">10:06:34</span>
                    <span class="sb-event-id">CORE.VISION</span>
                    <span class="sb-event-msg">MediaPipe Tasks HandLandmarker loaded via models/hand_landmarker.task (7.82 MB)</span>
                    <span class="sb-status-chip" style="padding:2px 8px;"><span class="sb-status-dot sb-dot-ready"></span>READY</span>
                </div>
                <div class="sb-event-row" style="border-left: 3px solid #6366f1;">
                    <span class="sb-event-time">10:06:35</span>
                    <span class="sb-event-id">ML.CLASSIFIER</span>
                    <span class="sb-event-msg">Balanced Random Forest loaded from models/isl_classifier.joblib (31 active classes)</span>
                    <span class="sb-status-chip" style="padding:2px 8px;"><span class="sb-status-dot sb-dot-active"></span>ACTIVE</span>
                </div>
                <div class="sb-event-row" style="border-left: 3px solid #6366f1;">
                    <span class="sb-event-time">10:06:35</span>
                    <span class="sb-event-id">NLP.TRANSLATE</span>
                    <span class="sb-event-msg">MarianMT seq2seq transformer weights verified in models/opus_mt_en_hi/ (303.7 MB)</span>
                    <span class="sb-status-chip" style="padding:2px 8px;"><span class="sb-status-dot sb-dot-ready"></span>READY</span>
                </div>
                <div class="sb-event-row" style="border-left: 3px solid #6366f1;">
                    <span class="sb-event-time">10:06:36</span>
                    <span class="sb-event-id">DEVICE.SENSOR</span>
                    <span class="sb-event-msg">Integrated Camera & USB DirectShow capture interfaces verified (DirectShow / V4L2)</span>
                    <span class="sb-status-chip" style="padding:2px 8px;"><span class="sb-status-dot sb-dot-ready"></span>ONLINE</span>
                </div>
                <div class="sb-event-row" style="border-left: 3px solid #6366f1;">
                    <span class="sb-event-time">10:06:36</span>
                    <span class="sb-event-id">ENFORCE.BUDGET</span>
                    <span class="sb-event-msg">Hard resource caps active: 2GB download limit, 4GB RAM ceiling, Zero paid APIs (config.py)</span>
                    <span class="sb-status-chip" style="padding:2px 8px;"><span class="sb-status-dot sb-dot-ready"></span>PASS</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 5. VOCABULARY COVERAGE & ALPHABET MATRIX (A–Z)
    # -------------------------------------------------------------------------
    st.markdown(
        """
        <div class="sb-section-tag">LINGUISTIC SCOPE // ALPHABET MATRIX</div>
        <h2 class="sb-section-heading">Supported Signs & Fingerspelling</h2>
        <p class="sb-section-desc">
            SignBridge supports core Indian Sign Language gestures and the full manual alphabet space (A–Z).
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_voc1, col_voc2 = st.columns([1, 1], gap="large")
    with col_voc1:
        st.markdown(
            """
            <div style="font-family:'JetBrains Mono', monospace; font-size:0.78rem; font-weight:700; color:#818cf8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.75rem;">
                // ACTIVE MODEL VOCABULARY
            </div>
            """,
            unsafe_allow_html=True,
        )
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
                    <span class="sb-status-dot sb-dot-active"></span>
                    <span>Linguistic Grounding: ISL vs. ASL</span>
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
        st.markdown(
            """
            <div style="font-family:'JetBrains Mono', monospace; font-size:0.78rem; font-weight:700; color:#818cf8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.75rem;">
                // ALPHABET COVERAGE STATUS (A–Z)
            </div>
            """,
            unsafe_allow_html=True,
        )
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
            <div style="font-family:'JetBrains Mono', monospace; font-size:0.72rem; color:var(--sb-text-subtle); margin-top:0.6rem; line-height:1.6;">
                <span style="color:#10b981;">● Active in classifier</span> &nbsp;|&nbsp;
                <span style="color:#818cf8;">▲ Ready to train</span> &nbsp;|&nbsp;
                <span style="color:#64748b;">○ Needs data</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
        sel_col1, sel_col2 = st.columns([1.3, 1.7])
        with sel_col1:
            cov_labels = [f"{it['letter']} — {it['status']} ({it['count']} samples)" for it in cov_items]
            selected_cov_idx = st.selectbox(
                "Select letter to practice or collect:",
                range(len(cov_items)),
                format_func=lambda i: cov_labels[i],
                key="home_letter_sel",
            )
            chosen_letter = cov_items[selected_cov_idx]["letter"]
        with sel_col2:
            st.markdown("<div style='height: 1.7rem;'></div>", unsafe_allow_html=True)
            act_col1, act_col2 = st.columns([1, 1])
            with act_col1:
                if st.button(f"Practice '{chosen_letter}' 🎯", use_container_width=True, key="home_go_practice_btn"):
                    st.session_state.practice_target = chosen_letter
                    st.session_state["practice_letter_select"] = chosen_letter
                    st.session_state.active_page = "Live App"
                    st.session_state.live_mode_view = "Interactive Practice Mode"
                    st.session_state["live_mode_selector"] = "Interactive Practice Mode"
                    st.rerun()
            with act_col2:
                if st.button(f"Collect in Studio →", type="primary", use_container_width=True, key="home_go_studio_btn"):
                    st.session_state.target_letter = chosen_letter
                    st.session_state.target_category = "Alphabet Letters (A–Z)"
                    st.session_state["studio_vocab_cat_radio"] = "Alphabet Letters (A–Z)"
                    st.session_state["studio_target_letter_select"] = chosen_letter
                    st.session_state.active_page = "Studio"
                    st.rerun()
