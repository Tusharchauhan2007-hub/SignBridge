"""
SignBridge — Complete Project Guide & College Viva Preparation PDF Generator.
Generates a comprehensive, beautifully styled academic and technical manual
covering all aspects of the SignBridge project.
"""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# 2-Pass Canvas for Accurate "Page X of Y" and Running Headers/Footers
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:  # Omit header/footer on title/cover page
            self.saveState()
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            # Running Top Header
            self.drawString(54, 748, "SignBridge — AI Sign Language Recognition & Offline Translation")
            self.setFont("Helvetica", 8)
            self.drawRightString(558, 748, "Complete Project Guide & Viva Manual")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, 740, 558, 740)

            # Running Bottom Footer
            self.line(54, 46, 558, 46)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 34, "Confidential Academic Documentation | Indian Sign Language (ISL) Assistant")
            self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
            self.restoreState()


def create_callout(text: str, title: str = "Hinglish Explanation & Mentor Tip", bg_hex: str = "#F8FAFC", border_hex: str = "#0284C7", style=None):
    """Creates a stylized, bordered callout box for easy reading."""
    content = [
        Paragraph(f"<b><font color='{border_hex}'>💡 {title}</font></b>", style),
        Spacer(1, 4),
        Paragraph(text, style)
    ]
    t = Table([[content]], colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_hex)),
        ('BOX', (0,0), (-1,-1), 1.0, colors.HexColor(border_hex)),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Hierarchy
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0369A1'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # =========================================================================
    # COVER / TITLE BANNER
    # =========================================================================
    story.append(Paragraph("<b>SignBridge</b>", title_style))
    story.append(Paragraph("<b>AI-Powered Real-Time Sign Language Recognition & Offline Translation Assistant</b>", ParagraphStyle('SubHeading', parent=title_style, fontSize=14, leading=18, textColor=colors.HexColor('#0284C7'))))
    story.append(Paragraph("Complete Comprehensive Project Guide, Architectural Specification & Viva Master Manual<br/><i>Prepared for College Project Presentations, Academic Defense & Technical Viva Voce</i>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=2, spaceAfter=12))

    # Metadata Grid
    meta_data = [
        [
            Paragraph("<b>Academic Subject:</b> AI / Computer Vision Project", table_cell_style),
            Paragraph("<b>Target Frameworks:</b> OpenCV, MediaPipe, Scikit-Learn, Streamlit", table_cell_style)
        ],
        [
            Paragraph("<b>Language:</b> Python 3.11", table_cell_style),
            Paragraph("<b>Vocabulary:</b> 31 Classes (26 Alphabet + 5 Word Gestures)", table_cell_style)
        ],
        [
            Paragraph("<b>Translation:</b> Offline MarianMT (English to Hindi)", table_cell_style),
            Paragraph("<b>TTS Engine:</b> Dual Offline (pyttsx3 + HTML5 Web Speech)", table_cell_style)
        ],
    ]
    meta_table = Table(meta_data, colWidths=[252, 252])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 1: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "Over 63 million people in India suffer from significant auditory impairment, relying predominantly on Indian Sign Language (ISL) for daily communication. Unfortunately, fewer than 1% of the general hearing population understands sign language, creating severe communication barriers in healthcare, banking, education, and social environments.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Existing Solutions & Their Flaws:</b> Most commercial translation tools rely on paid cloud APIs (e.g. Google Cloud Vision, OpenAI Whisper/Vision). These suffer from high recurring costs, critical privacy vulnerabilities (uploading private video streams to 3rd-party servers), and complete failure in low-connectivity or rural environments.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The SignBridge Solution:</b> SignBridge is a 100% offline, privacy-first assistive platform that runs directly on commodity laptops without external GPUs or cloud subscriptions. It captures standard 30 FPS webcam video, extracts 21 skeletal hand landmarks via MediaPipe Tasks, applies translation- and scale-invariant geometric normalization, classifies the gesture using a Random Forest classifier (99.0% accuracy), debounces tokens into fluent sentences, vocalizes text via dual Text-to-Speech engines, and translates English sentences into Devanagari Hindi via a local MarianMT neural network.",
        body_style
    ))

    story.append(create_callout(
        "<b>In Simple Words (Hinglish):</b> SignBridge ek aisa web assistant hai jo deaf ya mute logon ke hath ke signs ko laptop camera se dekh kar real-time me pehchanta hai. Ye na sirf signs ko text me jodta hai, balki use bol kar sunata hai (voice audio) aur saath hi bina internet ke Hindi me translate bhi kar deta hai!",
        "Mentor Note: The Core Philosophy",
        "#F0FDF4", "#16A34A", body_style
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 2: TECHNOLOGY STACK & LIBRARIES
    # =========================================================================
    story.append(Paragraph("2. Complete Technology Stack & Architecture", h1_style))
    story.append(Paragraph("Every component in SignBridge was chosen with precise engineering purpose to guarantee zero subscription costs and sub-50ms inference latency.", body_style))

    tech_data = [
        [
            Paragraph("<b>Technology</b>", table_header_style),
            Paragraph("<b>Purpose in SignBridge</b>", table_header_style),
            Paragraph("<b>Working Mechanism</b>", table_header_style),
            Paragraph("<b>Cost</b>", table_header_style)
        ],
        [
            Paragraph("<b>Python 3.11</b>", table_cell_style),
            Paragraph("Core programming runtime", table_cell_style),
            Paragraph("Compiles backend logic & bridges ML libraries", table_cell_style),
            Paragraph("Free / OSS", table_cell_style)
        ],
        [
            Paragraph("<b>OpenCV</b>", table_cell_style),
            Paragraph("Webcam video acquisition & overlay", table_cell_style),
            Paragraph("Reads 30 FPS frames & draws hand landmark skeleton", table_cell_style),
            Paragraph("Free / OSS", table_cell_style)
        ],
        [
            Paragraph("<b>MediaPipe Tasks</b>", table_cell_style),
            Paragraph("21 3D hand landmark detection", table_cell_style),
            Paragraph("Loads hand_landmarker.task; outputs x,y,z coordinates", table_cell_style),
            Paragraph("Free (Google)", table_cell_style)
        ],
        [
            Paragraph("<b>NumPy</b>", table_cell_style),
            Paragraph("Geometric math & normalization", table_cell_style),
            Paragraph("Computes Euclidean distances & 63D feature vectors", table_cell_style),
            Paragraph("Free / OSS", table_cell_style)
        ],
        [
            Paragraph("<b>Pandas</b>", table_cell_style),
            Paragraph("Dataset storage & management", table_cell_style),
            Paragraph("Reads/writes data/isl_dataset.csv with session metadata", table_cell_style),
            Paragraph("Free / OSS", table_cell_style)
        ],
        [
            Paragraph("<b>Scikit-Learn</b>", table_cell_style),
            Paragraph("Random Forest classifier", table_cell_style),
            Paragraph("Ensemble of 150 Decision Trees classifying 31 gestures", table_cell_style),
            Paragraph("Free / OSS", table_cell_style)
        ],
        [
            Paragraph("<b>Joblib</b>", table_cell_style),
            Paragraph("Model persistence & loading", table_cell_style),
            Paragraph("Serializes trained model artifact to models/isl_classifier.joblib", table_cell_style),
            Paragraph("Free / OSS", table_cell_style)
        ],
        [
            Paragraph("<b>Streamlit</b>", table_cell_style),
            Paragraph("Frontend UI & routing", table_cell_style),
            Paragraph("Reactive web interface with dark/light themes & session state", table_cell_style),
            Paragraph("Free / OSS", table_cell_style)
        ],
        [
            Paragraph("<b>MarianMT (Transformers)</b>", table_cell_style),
            Paragraph("Offline English-to-Hindi translation", table_cell_style),
            Paragraph("Local Seq2Seq neural network (Helsinki-NLP/opus-mt-en-hi)", table_cell_style),
            Paragraph("Free / OSS", table_cell_style)
        ],
        [
            Paragraph("<b>pyttsx3 & Web Speech</b>", table_cell_style),
            Paragraph("Dual Text-to-Speech audio", table_cell_style),
            Paragraph("Threaded native OS voice + browser HTML5 synthesis", table_cell_style),
            Paragraph("Free / Local", table_cell_style)
        ],
        [
            Paragraph("<b>Pytest</b>", table_cell_style),
            Paragraph("Automated test suite (52 tests)", table_cell_style),
            Paragraph("Validates invariance, bounds, dataset schema & routing", table_cell_style),
            Paragraph("Free / OSS", table_cell_style)
        ],
    ]
    tech_table = Table(tech_data, colWidths=[90, 115, 235, 64])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 3: COMPLETE END-TO-END WORKFLOW
    # =========================================================================
    story.append(Paragraph("3. Complete End-to-End Workflow & Pipeline", h1_style))
    story.append(Paragraph("The system functions through a 7-stage real-time execution loop executed every ~33 milliseconds:", body_style))

    story.append(Paragraph("<b>Stage 1: Video Ingestion & Skeleton Extraction:</b> OpenCV reads BGR video frames. MediaPipe Tasks HandLandmarker locates the hand bounding box and extracts 21 3D landmark points (x, y, z relative to camera viewport). If no hand is present, the frame gracefully outputs a 'Searching for hand' status without crashing.", bullet_style))
    story.append(Paragraph("<b>Stage 2: Geometric Preprocessing (Normalization):</b> Raw pixel coordinates vary based on distance and hand position. The system performs two mathematical operations: (1) Wrist-relative translation (shifting Landmark 0 to origin), and (2) Scale normalization (dividing by the Euclidean distance between wrist 0 and middle MCP knuckle 9). This yields 63 invariant float32 features.", bullet_style))
    story.append(Paragraph("<b>Stage 3: Random Forest Inference:</b> The 63 features are fed to the pre-trained Random Forest model. It evaluates probabilities across all 31 target classes in under 2ms on CPU.", bullet_style))
    story.append(Paragraph("<b>Stage 4: Confidence Gating & Anti-Flicker Temporal Window:</b> If predicted confidence is below 60% (0.60), the prediction is rejected as ambiguous. A 7-frame rolling FIFO queue maintains recent predictions; only when a class wins the majority vote (>55% agreement) over 7 frames is the gesture accepted as stable.", bullet_style))
    story.append(Paragraph("<b>Stage 5: Sentence Composition & Debouncing:</b> The debounced gesture token is dispatched to the SentenceBuilder. A 1.2-second cooldown timer ensures continuous hand presence does not flood identical tokens (e.g., prevents appending 'AAAAA' in 1 second). Letters seamlessly concatenate into words; spaces and backspaces allow full conversational editing.", bullet_style))
    story.append(Paragraph("<b>Stage 6: Multi-Modal Audio Vocalization:</b> The assembled sentence is vocalized aloud using dual speech synthesis: either the native OS speech synthesizer via a dedicated pyttsx3 worker thread, or directly in-browser using the HTML5 Web Speech API.", bullet_style))
    story.append(Paragraph("<b>Stage 7: Offline Neural Hindi Translation:</b> The composed English sentence is processed by MarianMT running locally on CPU. It tokenizes English text and generates fluent Hindi Devanagari script (e.g. 'HELLO HELP' ➔ 'नमस्ते मदद') with zero internet connection.", bullet_style))

    # Flowchart Box
    flowchart_text = """
    [ Webcam Input (OpenCV) ] ──► [ MediaPipe HandLandmarker ] ──► [ 21 3D Joints ]
                                                                          │
    [ 63 Invariant Features ] ◄── [ Math Normalization: Wrist Rel & Scale ]
             │
             ▼
    [ Random Forest Classifier ] ──► [ Confidence Gate > 60% ] ──► [ 7-Frame Majority Smoothing ]
                                                                             │
    [ Dual Audio TTS (pyttsx3/WebSpeech) ] ◄── [ Sentence Builder (1.2s Cooldown) ] ──► [ MarianMT Hindi Translation ]
    """
    flowchart_table = Table([[Paragraph(f"<pre>{flowchart_text.strip()}</pre>", code_style)]], colWidths=[504])
    flowchart_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(flowchart_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 4: PROJECT DIRECTORY & IMPORTANT FILES TABLE
    # =========================================================================
    story.append(Paragraph("4. Project Directory & Important Files Reference", h1_style))
    story.append(Paragraph("SignBridge strictly separates presentation (frontend) from computational ML logic (backend):", body_style))

    files_data = [
        [
            Paragraph("<b>File / Directory</b>", table_header_style),
            Paragraph("<b>Architectural Purpose</b>", table_header_style),
            Paragraph("<b>Key Functions / Classes</b>", table_header_style),
            Paragraph("<b>Interconnection</b>", table_header_style)
        ],
        [
            Paragraph("<b>app.py</b>", table_cell_style),
            Paragraph("Root launcher & Windows runtime wrapper", table_cell_style),
            Paragraph("Pre-loads torch, adds C-DLL paths, calls frontend_main()", table_cell_style),
            Paragraph("Primary entry point for Streamlit", table_cell_style)
        ],
        [
            Paragraph("<b>frontend/app.py</b>", table_cell_style),
            Paragraph("Presentation orchestrator & router", table_cell_style),
            Paragraph("init_app_session_state(), main(), cached resource getters", table_cell_style),
            Paragraph("Connects navbar to pages & backend", table_cell_style)
        ],
        [
            Paragraph("<b>frontend/pages/live_app.py</b>", table_cell_style),
            Paragraph("Live recognition & practice workspace", table_cell_style),
            Paragraph("render_live_app_page(), camera loops, telemetry cards", table_cell_style),
            Paragraph("Consumes predictor & tracker", table_cell_style)
        ],
        [
            Paragraph("<b>frontend/pages/studio.py</b>", table_cell_style),
            Paragraph("Dataset collection & model trainer", table_cell_style),
            Paragraph("render_studio_page(), sample recording, train triggers", table_cell_style),
            Paragraph("Calls DatasetManager & train_model", table_cell_style)
        ],
        [
            Paragraph("<b>frontend/styles/theme.py</b>", table_cell_style),
            Paragraph("CSS design system & theme tokens", table_cell_style),
            Paragraph("get_theme_css(theme), palette injection, high contrast", table_cell_style),
            Paragraph("Injected across all UI pages", table_cell_style)
        ],
        [
            Paragraph("<b>backend/preprocessing.py</b>", table_cell_style),
            Paragraph("Mathematical invariance & 63D features", table_cell_style),
            Paragraph("LandmarkPreprocessor, normalize(), extract_from_landmarks()", table_cell_style),
            Paragraph("Used by tracker, predictor, & studio", table_cell_style)
        ],
        [
            Paragraph("<b>backend/hand_tracking.py</b>", table_cell_style),
            Paragraph("MediaPipe Tasks HandLandmarker wrapper", table_cell_style),
            Paragraph("HandTracker, detect(), draw_landmarks()", table_cell_style),
            Paragraph("Supplies coordinates to preprocessor", table_cell_style)
        ],
        [
            Paragraph("<b>backend/predictor.py</b>", table_cell_style),
            Paragraph("Inference engine with confidence gating", table_cell_style),
            Paragraph("SignPredictor, predict(), 7-frame smoothing queue", table_cell_style),
            Paragraph("Consumes models/isl_classifier.joblib", table_cell_style)
        ],
        [
            Paragraph("<b>backend/data_collection.py</b>", table_cell_style),
            Paragraph("Dataset manager & CSV persistence", table_cell_style),
            Paragraph("DatasetManager, append_sample(), get_class_counts()", table_cell_style),
            Paragraph("Reads/writes data/isl_dataset.csv", table_cell_style)
        ],
        [
            Paragraph("<b>backend/text_to_speech.py</b>", table_cell_style),
            Paragraph("Sentence composition & dual TTS", table_cell_style),
            Paragraph("SentenceBuilder, speak_text(), append_token()", table_cell_style),
            Paragraph("Drives live app transcription", table_cell_style)
        ],
        [
            Paragraph("<b>backend/translator.py</b>", table_cell_style),
            Paragraph("Offline neural English-to-Hindi MT", table_cell_style),
            Paragraph("EnglishToHindiTranslator, translate(), load()", table_cell_style),
            Paragraph("Consumes models/opus_mt_en_hi", table_cell_style)
        ],
        [
            Paragraph("<b>frontend/utils/command_manager.py</b>", table_cell_style),
            Paragraph("Custom personal gesture commands", table_cell_style),
            Paragraph("CustomCommandManager, execute_command(), JSON storage", table_cell_style),
            Paragraph("Triggers macros on HELP/HELLO", table_cell_style)
        ],
    ]
    files_table = Table(files_data, colWidths=[95, 115, 155, 139])
    files_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(files_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 5: SOURCE CODE DEEP DIVE & MATHEMATICAL FORMULAS
    # =========================================================================
    story.append(Paragraph("5. Source Code Deep Dive & Mathematical Formulations", h1_style))

    story.append(Paragraph("5.1 Mathematical Normalization (backend/preprocessing.py)", h2_style))
    story.append(Paragraph("Raw coordinates from computer vision vary dramatically if a signer sits 1 meter vs 2 meters from the camera, or shifts from left to right. Normalization solves this:", body_style))
    story.append(Paragraph("<b>1. Translation Invariance (Shift to Origin):</b> Let Landmark 0 be the wrist joint with coordinates P_0 = (x_0, y_0, z_0). For all 21 landmarks P_i (where i = 0 ... 20), we compute: <br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>P'_i = P_i - P_0</b><br/>This makes the wrist the coordinate origin (0, 0, 0), eliminating hand placement position from the equation.", bullet_style))
    story.append(Paragraph("<b>2. Scale Invariance (Normalized Hand Span):</b> The distance from the wrist (Joint 0) to the middle finger MCP joint (Joint 9) represents hand size. We compute the Euclidean norm: <br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>d_scale = || P_9 - P_0 || = sqrt((x_9 - x_0)^2 + (y_9 - y_0)^2 + (z_9 - z_0)^2)</b><br/>All translated points are normalized by this distance: <b>P''_i = P'_i / d_scale</b>. (With safety epsilon 1e-4 preventing division by zero).", bullet_style))
    story.append(Paragraph("<b>3. Flattening:</b> The resulting 21 3D points are flattened into a 1D float32 array: [lm_0_x, lm_0_y, lm_0_z, ..., lm_20_z] containing exactly <b>63 features</b>.", bullet_style))

    story.append(Paragraph("5.2 Anti-Flicker Temporal Window & Confidence Gating (backend/predictor.py)", h2_style))
    story.append(Paragraph(
        "Single-frame computer vision predictions suffer from high-frequency jitter (rapidly toggling between visually similar letters like 'M' and 'N'). SignBridge solves this through a dual-stage filter:",
        body_style
    ))
    story.append(Paragraph("<b>1. Confidence Threshold Gating:</b> The Random Forest outputs probability vector P over all 31 classes. If max(P) < 0.60, the prediction is classified as invalid ('Low confidence - hold steady').", bullet_style))
    story.append(Paragraph("<b>2. Majority Voting Smoothing:</b> Valid predictions enter a FIFO deque of size W=7. The final reported label is: <br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>Label_final = mode(queue)</b> if <b>count(mode(queue)) / W >= 0.55</b><br/>This guarantees that only stable gestures held for at least 4-5 consecutive frames (~150ms) are recognized.", bullet_style))

    story.append(Paragraph("5.3 Debounced Sentence Composition (backend/text_to_speech.py)", h2_style))
    story.append(Paragraph(
        "A video stream processes ~30 frames/sec. If a signer displays the letter 'A' for 1 second, a naive system would produce 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'. SignBridge uses a <b>1.2-second cooldown debouncer</b>:",
        body_style
    ))
    story.append(Paragraph("<b>Debounce Rule:</b> If token == last_token, require <b>(current_time - last_added_time) >= 1.2 seconds</b> before re-appending. If the user transitions to a different sign, the cooldown immediately resets.", bullet_style))

    story.append(Paragraph("5.4 Offline MarianMT Neural Translation (backend/translator.py)", h2_style))
    story.append(Paragraph(
        "Offline translation loads the MarianMT Seq2Seq Transformer model from `models/opus_mt_en_hi`. It executes entirely on CPU via PyTorch. English sentences are tokenized with SentencePiece, passed through 6 encoder-decoder layers, and decoded into Devanagari Hindi using beam search.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 6: MACHINE LEARNING & DATASET
    # =========================================================================
    story.append(Paragraph("6. Machine Learning Pipeline & Dataset Metrics", h1_style))
    story.append(Paragraph(
        "<b>Linguistic Distinction (ISL vs ASL):</b> American Sign Language (ASL) uses a single-handed manual alphabet derived from French Sign Language. Indian Sign Language (ISL), officially codified by ISLRTC, traditionally uses a two-handed manual alphabet. For single-camera desktop compatibility, dominant hand configurations and standard ISL gestures are recorded.",
        body_style
    ))
    story.append(Paragraph("<b>Trained Classes:</b> 31 Classes total — 26 Alphabet letters (A to Z) + 5 Core Words (HELLO, HELP, NO, THANK_YOU, YES).", body_style))

    metrics_data = [
        [Paragraph("<b>Metric</b>", table_header_style), Paragraph("<b>Value</b>", table_header_style), Paragraph("<b>Significance for Project Viva</b>", table_header_style)],
        [Paragraph("Total Dataset Samples", table_cell_style), Paragraph("2,093 samples", table_cell_style), Paragraph("Real recorded geometric landmarks stored in CSV", table_cell_style)],
        [Paragraph("Number of Estimators", table_cell_style), Paragraph("150 Decision Trees", table_cell_style), Paragraph("High variance reduction without overfitting", table_cell_style)],
        [Paragraph("Test Accuracy", table_cell_style), Paragraph("<b>99.05%</b>", table_cell_style), Paragraph("Stratified evaluation across all 31 gesture classes", table_cell_style)],
        [Paragraph("Macro Precision", table_cell_style), Paragraph("<b>99.09%</b>", table_cell_style), Paragraph("Low false-positive rate across every individual letter", table_cell_style)],
        [Paragraph("Macro Recall", table_cell_style), Paragraph("<b>99.50%</b>", table_cell_style), Paragraph("Extremely low false-negative rate (rarely misses a sign)", table_cell_style)],
        [Paragraph("Macro F1-Score", table_cell_style), Paragraph("<b>99.27%</b>", table_cell_style), Paragraph("Harmonic mean confirming balance across classes", table_cell_style)],
        [Paragraph("Inference Time", table_cell_style), Paragraph("~1.2 ms / sample", table_cell_style), Paragraph("Leaves 96% of CPU budget for rendering and video", table_cell_style)],
    ]
    metrics_table = Table(metrics_data, colWidths=[130, 95, 279])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 7: HOW TO RUN & TROUBLESHOOT
    # =========================================================================
    story.append(Paragraph("7. Setup, Execution & Troubleshooting Guide", h1_style))
    story.append(Paragraph("<b>Exact Steps to Run the Project on Windows 11:</b>", body_style))
    story.append(Paragraph("1. Open PowerShell and navigate to the project directory: <code>cd d:\\vs_code\\innotech</code>", bullet_style))
    story.append(Paragraph("2. Launch the Streamlit application: <code>.\\.venv\\Scripts\\streamlit.exe run app.py</code>", bullet_style))
    story.append(Paragraph("3. The browser will automatically open to <code>http://localhost:8501</code>. Navigate to 'Live App' and allow camera access.", bullet_style))
    story.append(Paragraph("4. To execute the automated verification test suite: <code>.\\.venv\\Scripts\\pytest.exe -v</code> (52 passed in ~37s).", bullet_style))

    trouble_data = [
        [Paragraph("<b>Common Error / Issue</b>", table_header_style), Paragraph("<b>Root Cause</b>", table_header_style), Paragraph("<b>Solution Applied</b>", table_header_style)],
        [
            Paragraph("WinError 4551 (SAC Block)", table_cell_style),
            Paragraph("Windows Smart App Control blocks unsigned dev wheels", table_cell_style),
            Paragraph("Pinned pandas==2.2.3 and added os.add_dll_directory in app.py", table_cell_style)
        ],
        [
            Paragraph("WinError 1114 (DLL init fail)", table_cell_style),
            Paragraph("OpenMP/c10 conflict between PyTorch & MediaPipe", table_cell_style),
            Paragraph("Pre-imported `torch` in app.py before OpenCV/MediaPipe", table_cell_style)
        ],
        [
            Paragraph("Webcam screen is black", table_cell_style),
            Paragraph("Camera index 0 occupied by Zoom/Teams/Browser", table_cell_style),
            Paragraph("Close other camera apps or switch camera index in settings", table_cell_style)
        ],
    ]
    trouble_table = Table(trouble_data, colWidths=[130, 160, 214])
    trouble_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(trouble_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 8: COLLEGE PRESENTATION & PITCH GUIDE
    # =========================================================================
    story.append(Paragraph("8. College Presentation Script & Pitch Guide", h1_style))

    story.append(Paragraph("8.1 The 1-Minute Elevator Pitch", h2_style))
    pitch_text = (
        "\"Good morning respected professors and evaluators. Our project is <b>SignBridge</b> — an AI-powered assistive communication platform that translates Indian Sign Language into real-time speech and Hindi text.<br/><br/>"
        "Over 63 million people in India have hearing loss, but less than 1% of hearing people know sign language. Existing apps rely on expensive cloud APIs that compromise privacy and fail without internet. SignBridge solves this by running <b>100% locally on a standard laptop webcam</b>. It tracks 21 hand joints via MediaPipe, normalizes them for hand size and camera distance, classifies 31 signs using a 99% accurate Random Forest model, speaks sentences aloud, and translates them into Hindi using a local neural model. Thank you!\""
    )
    story.append(create_callout(pitch_text, "1-Minute Project Pitch", "#F8FAFC", "#0284C7", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("8.2 Detailed 3–5 Minute Presentation Outline", h2_style))
    story.append(Paragraph("<b>Slide 1: Title & Problem:</b> Introduce SignBridge. Highlight the 63M Indian population with auditory impairment and the acute lack of human interpreters.", bullet_style))
    story.append(Paragraph("<b>Slide 2: System Architecture:</b> Walk through the 7-stage pipeline: Webcam ➔ MediaPipe ➔ Math Normalization (63 features) ➔ Random Forest ➔ Temporal Smoothing ➔ Dual TTS & MarianMT Hindi.", bullet_style))
    story.append(Paragraph("<b>Slide 3: Technical Highlights:</b> Explain Wrist-Relative Translation & Scale Invariance. Emphasize why geometric landmarks are superior to raw CNN pixels (immune to skin tone and background lighting).", bullet_style))
    story.append(Paragraph("<b>Slide 4: Live Demonstration:</b> Show fingerspelling forming a word, sentence controls (Space/Backspace), audio synthesis, and offline Hindi translation.", bullet_style))
    story.append(Paragraph("<b>Slide 5: Metrics & Results:</b> Present 99.05% accuracy across 2,093 samples and 52 passed unit tests. Conclude with zero cloud costs and complete privacy.", bullet_style))
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 9: MASTER VIVA QUESTIONS & ANSWERS (35+ Q&A)
    # =========================================================================
    story.append(Paragraph("9. Master Viva Voce Preparation (35 Questions & Answers)", h1_style))
    story.append(Paragraph("Below are the exact questions professors, external examiners, and technical evaluators ask, complete with crisp, bulletproof answers:", body_style))

    viva_qa = [
        ("Q1: What is the primary objective of SignBridge?",
         "SignBridge enables two-way communication between deaf/mute individuals using Indian Sign Language and hearing individuals by converting hand signs into real-time spoken audio and offline Hindi translation."),

        ("Q2: Why did you choose MediaPipe over training a raw CNN (like ResNet or YOLO)?",
         "A raw CNN is sensitive to background clutter, room lighting, skin tone, and clothing. MediaPipe abstracts the hand into 21 pure geometric joint coordinates, eliminating visual bias, reducing memory footprint, and running at 30+ FPS on standard CPU without GPUs."),

        ("Q3: What are the 63 features used in classification?",
         "MediaPipe outputs 21 landmarks, each with 3 spatial coordinates (x, y, z). 21 × 3 = 63 numerical features representing the spatial skeleton of the hand."),

        ("Q4: How do you achieve Translation Invariance?",
         "We subtract the wrist coordinate (Landmark 0) from all other 20 landmarks: P'_i = P_i - P_0. This shifts the hand's reference origin to (0,0,0) regardless of where the hand is positioned on the camera screen."),

        ("Q5: How do you achieve Scale Invariance?",
         "We compute the Euclidean distance between the wrist (Landmark 0) and the middle finger MCP joint (Landmark 9). All coordinates are divided by this distance, so hand size or distance from the camera does not alter the geometric representation."),

        ("Q6: Why Random Forest instead of an SVM, KNN, or Deep Neural Network?",
         "For a tabular 63-feature dataset, Random Forest trains in seconds, handles non-linear relationships across joint angles effortlessly, does not require feature scaling, provides class probabilities, and resists overfitting through bagging across 150 trees."),

        ("Q7: How many classes can your trained model recognize?",
         "31 classes: all 26 manual alphabet letters (A to Z) plus 5 core Indian Sign Language words (HELLO, HELP, NO, THANK_YOU, YES)."),

        ("Q8: What is Confidence Gating and why is it set to 60%?",
         "If the Random Forest's highest predicted probability is under 0.60, the system rejects the prediction as ambiguous. This prevents random guessing when the user transitions between signs or moves their hand."),

        ("Q9: What is the purpose of the 7-Frame Rolling Window?",
         "Single-frame video predictions can flicker between similar letters due to micro-movements. The 7-frame queue takes a majority vote; a sign is only accepted if it wins >=55% of the last 7 frames, ensuring stable recognition."),

        ("Q10: What is the Cooldown Debouncer in the SentenceBuilder?",
         "At 30 FPS, holding a hand for 1 second produces 30 detections. The 1.2s cooldown timer prevents repeating the same token repeatedly while allowing instant appending of new, distinct tokens."),

        ("Q11: How does the offline Hindi translation work without internet?",
         "We package a local Hugging Face MarianMT model (Helsinki-NLP/opus-mt-en-hi) in the models/ directory. A Seq2Seq Transformer model runs locally on CPU with zero network calls, converting English tokens into Devanagari Hindi."),

        ("Q12: Why do you have a 'Dual TTS' engine?",
         "pyttsx3 runs on a native background OS thread for desktop audio, while HTML5 Web Speech API synthesizes audio directly inside the web browser. If one fails or lacks system drivers, the other serves as an automatic fallback."),

        ("Q13: How did you prevent Data Leakage during model training?",
         "We use GroupShuffleSplit based on 'session_id'. Samples from the same recording session never appear in both training and test sets, ensuring the model generalizes to unseen sessions rather than memorizing a specific recording."),

        ("Q14: What is the difference between ISL and ASL?",
         "American Sign Language (ASL) uses a single-handed alphabet based on French Sign Language. Indian Sign Language (ISL), codified by ISLRTC, traditionally utilizes two-handed alphabets based on the British BANZSL family. SignBridge adapts single-handed dominant postures for single-camera desktop convenience."),

        ("Q15: How does the Studio page work?",
         "The Studio page allows users to record genuine ISL samples for any letter (A-Z) or word. It records 63-feature coordinates, saves metadata to data/isl_dataset.csv, and allows retraining the Random Forest model with one click."),

        ("Q16: How do you handle cases where no hand is visible?",
         "MediaPipe returns an empty landmark list. The system catches this, resets temporal buffers, displays a 'Searching for hand...' status badge, and executes zero inference calls, conserving CPU power."),

        ("Q17: What is Streamlit session_state?",
         "Streamlit re-executes the entire Python script upon every user interaction (button click, slider move). session_state is a persistent dictionary that preserves variables (sentence builder, active theme, history) across reruns."),

        ("Q18: What are Custom Gesture Commands?",
         "Users can map specific gestures (like HELP or HELLO) to macro actions (like speaking an urgent emergency phrase or triggering Hindi translation) defined in data/custom_commands.json."),

        ("Q19: How do you verify code quality in SignBridge?",
         "We maintain an automated test suite of 52 unit and integration tests using Pytest, covering preprocessing invariance, dataset schema, budget enforcement, translation, and UI logic (100% pass rate)."),

        ("Q20: What are the current limitations of the project?",
         "1. It operates primarily on single-hand signs (dominant hand). 2. It classifies static postures rather than complex dynamic signs with trajectory motion. 3. It requires reasonable camera exposure without severe motion blur."),

        ("Q21: How would you extend SignBridge for dynamic gestures (like waving or complex phrases)?",
         "By introducing a temporal deep learning model such as an LSTM, GRU, or 1D-CNN that ingests a sequence of landmark frames (e.g. 30 consecutive frames) to classify trajectory and hand motion over time."),

        ("Q22: Why did you create separate frontend and backend directories?",
         "Architectural separation of concerns: backend modules can be imported into mobile apps, CLI scripts, or REST APIs without depending on Streamlit UI code."),

        ("Q23: What is the purpose of the src/ directory?",
         "src/ contains re-export shims that point to backend modules to ensure 100% backwards compatibility with earlier scripts and tests."),

        ("Q24: How much memory (RAM) does SignBridge consume?",
         "The Random Forest model is ~11 MB, MediaPipe task is ~8 MB, and the MarianMT model is ~300 MB. Total operational memory footprint is under 600 MB of RAM, easily running on 4GB or 8GB laptops."),

        ("Q25: What is the time complexity of the Random Forest inference?",
         "O(M * D), where M is the number of trees (150) and D is the maximum depth of each tree (~15-20). This takes approximately 1.2 milliseconds on CPU."),

        ("Q26: What is Zip Slip and how did you protect against it?",
         "Zip Slip is a path traversal vulnerability where malicious zip files extract files outside the target directory using '../'. We implemented canonical path validation in prepare_dataset.py."),

        ("Q27: What is the role of joblib?",
         "Joblib serializes Python objects with large NumPy arrays efficiently using memory mapping, enabling instantaneous loading of our trained model."),

        ("Q28: How does the application support accessibility in its UI?",
         "High-contrast color palettes (light/dark mode), large scalable typography, visual status badges, and dual audio/visual feedback ensure accessibility for individuals with various sensory impairments."),

        ("Q29: Can this model recognize signs from someone wearing gloves or jewelry?",
         "Yes, because MediaPipe's neural network tracks skeletal joint structures and depths rather than relying on skin-tone color segmentations."),

        ("Q30: What happens if two hands enter the webcam frame?",
         "HandTracker is initialized with max_num_hands=1, prioritizing the primary/dominant hand with highest detection score, preventing feature dimension mismatch."),

        ("Q31: What is MarianTokenizer?",
         "A SentencePiece subword tokenizer that converts English character strings into numerical token IDs mapped to the MarianMT bilingual vocabulary dictionary."),

        ("Q32: Why did you include automated py_compile checks?",
         "py_compile checks Python bytecode compilation across all 47 project files to guarantee zero syntax errors before deployment or test execution."),

        ("Q33: How does Practice Mode help learners?",
         "Practice Mode prompts users with target alphabet letters, compares real-time signs against the target, and provides instant visual feedback and score tracking."),

        ("Q34: How is model accuracy evaluated?",
         "Through stratified train-test splitting and cross-validation, computing accuracy, precision, recall, and F1-score across all 31 classes (current accuracy: 99.05%)."),

        ("Q35: What is the future vision for SignBridge?",
         "Deploying as a lightweight mobile app, integrating two-hand continuous ISL recognition via temporal Transformers, and incorporating two-way speech-to-sign 3D avatar animations.")
    ]

    for q, a in viva_qa:
        q_item = [
            Paragraph(f"<b><font color='#0369A1'>{q}</font></b>", h3_style),
            Paragraph(a, body_style),
            Spacer(1, 4)
        ]
        story.append(KeepTogether(q_item))

    # =========================================================================
    # BUILD DOCUMENT
    # =========================================================================
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent
    pdf_file = str(out_dir / "SignBridge_Complete_Project_Guide.pdf")
    build_pdf(pdf_file)

