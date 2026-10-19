# SignBridge — Communication without barriers.

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![MediaPipe Tasks](https://img.shields.io/badge/MediaPipe-Tasks%20API-orange.svg)](https://developers.google.com/mediapipe)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.66.0-red.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-RandomForest-green.svg)](https://scikit-learn.org/)
[![pytest](https://img.shields.io/badge/pytest-passing-brightgreen.svg)](https://pytest.org/)

**SignBridge** is a modern accessibility technology platform engineered for real-time sign language recognition and assisted everyday communication. Built with a human-centered product aesthetic, SignBridge translates hand signs and fingerspelling through standard laptop webcams into text sentences and spoken audio.


---

## 📌 Table of Contents
1. [Project Objectives & Scope](#-project-objectives--scope)
2. [Machine Learning & CV Architecture](#-machine-learning--cv-architecture)
3. [Technology Stack](#-technology-stack)
4. [Indian Sign Language (ISL) Vocabulary](#-indian-sign-language-isl-vocabulary)
5. [Project Structure](#-project-structure)
6. [Windows 11 Step-by-Step Setup Guide](#-windows-11-step-by-step-setup-guide)
7. [Running the Application](#-running-the-application)
8. [Automated Test Suite & Results](#-automated-test-suite--results)
9. [Key Features & Accessibility Design](#-key-features--accessibility-design)
10. [Known Limitations & Future Roadmap](#-known-limitations--future-roadmap)
11. [Verification Checklist](#-verification-checklist)

---

## 🎯 Project Objectives & Scope

- **Primary Goal**: Translate static hand gestures into clear text and natural vocalized speech in real-time.
- **Scope**: Focuses on a defined, clearly documented vocabulary of **Indian Sign Language (ISL)** static signs (`HELLO`, `YES`, `NO`, `THANK_YOU`, `HELP`), with capabilities to record and train custom signs directly within the app.
- **Integrity Principle**: No fabricated predictions or synthetic data claiming to be genuine observations. When confidence is insufficient or no hand is present, the system transparently indicates its state.

---

## 🏗️ Machine Learning & CV Architecture

```
┌─────────────────┐
│  Webcam Stream  │ (OpenCV BGR video capture at ~30 FPS)
└────────┬────────┘
         ▼
┌─────────────────┐
│ MediaPipe Tasks │ (Google MediaPipe Tasks HandLandmarker)
│ HandLandmarker  │ 21 3D points: wrist, MCP, PIP, DIP, fingertips
└────────┬────────┘
         ▼
┌─────────────────┐
│  Preprocessing  │ 1. Wrist Translation Invariance: shift coords relative to landmark 0
│ & Normalization │ 2. Scale Invariance: normalize by distance between wrist & middle MCP (9)
│   (63 Features) │ 3. Output: 63 float32 features [lm_0_x, ..., lm_20_z]
└────────┬────────┘
         ▼
┌─────────────────┐
│  Random Forest  │ Multiclass Random Forest with balanced class weights
│   Classifier    │ Evaluated via GroupShuffleSplit to prevent recording session leakage
└────────┬────────┘
         ▼
┌─────────────────┐
│ Confidence &    │ 1. Confidence Threshold Gating (default >60%)
│ Window Smoothing│ 2. Rolling Window (7 frames) majority-vote debouncing
└────────┬────────┘
         ▼
┌─────────────────┐
│ Sentence Builder│ Debounce cooldown timer, token appending, spacing, and backspace
└────────┬────────┘
         ▼
┌─────────────────┐
│ Dual Audio TTS  │ 1. Native background thread pyttsx3 engine
│  & Text Output  │ 2. Client-side HTML5 Web Speech API for universal browser audio
└─────────────────┘
```

---

## 💻 Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.11** | Backend computational runtime & ML pipeline |
| **OpenCV (`opencv-python`)** | Real-time webcam frame acquisition, video rendering, and skeleton overlay |
| **MediaPipe Tasks API** | State-of-the-art HandLandmarker (`hand_landmarker.task`) for 21 3D landmarks |
| **NumPy & Pandas** | Geometric vector transformations, dataset manipulation, and CSV storage |
| **scikit-learn** | Random Forest Classifier, group-aware cross-validation, and metrics evaluation |
| **Streamlit** | Responsive, high-contrast, modern interactive web interface |
| **joblib** | Model and metadata serialization / deserialization |
| **pyttsx3 & Web Speech API** | Dual offline + in-browser speech synthesis |
| **pytest** | Automated unit and integration testing suite |

---

## 🤟 Supported Indian Sign Language (ISL) Vocabulary & Alphabet

### 1. Core Word Gestures (Trained & Active)
| Sign Label | Description | Handshape Configuration |
| :--- | :--- | :--- |
| **`HELLO`** | Standard greeting / open hand | Flat palm facing forward, all fingers and thumb extended |
| **`YES`** | Agreement / confirmation | Closed fist with thumb extended upwards in vertical posture |
| **`NO`** | Disagreement / negation | Index and middle fingers extended together horizontally; ring and pinky curled |
| **`THANK_YOU`** | Gratitude | Open flat hand with palm facing slightly upward/forward |
| **`HELP`** | Requesting assistance | Closed fist with thumb up resting on or upright in signing space |

### 2. Manual Alphabet (A–Z Fingerspelling)
SignBridge's pipeline supports the full alphabet space from **A to Z** (31 total target classes):
`A`, `B`, `C`, `D`, `E`, `F`, `G`, `H`, `I`, `J`, `K`, `L`, `M`, `N`, `O`, `P`, `Q`, `R`, `S`, `T`, `U`, `V`, `W`, `X`, `Y`, `Z`.

- **Current Status**: A–Z labels are fully integrated into the data collection module, training pipeline, real-time prediction engine, and word-concatenating sentence builder.
- **Data Status**: The active pre-trained model contains the 5 core ISL word signs (`HELLO`, `YES`, `NO`, `THANK_YOU`, `HELP`). The letters A–Z are ready for genuine collection and training via the **Dataset Collection** page.

### 🇮🇳 Linguistic Verification: ISL vs ASL
> **Critical Distinction**: Indian Sign Language (ISL) is **linguistically distinct** from American Sign Language (ASL).
> - **ASL** uses a **one-handed manual alphabet** derived from the French Sign Language system.
> - **ISL**, as officially codified by the **Indian Sign Language Research and Training Centre (ISLRTC)**, historically employs a **two-handed manual alphabet** related to the British Sign Language (BANZSL) family.
> - For single-camera single-hand detection, single-handed fingerspelling conventions or dominant-hand postures are captured. **Do not assume ASL and ISL handshapes are interchangeable.**


---

## 📂 Project Structure

```
innotech/
├── app.py                      # Root launcher & Windows PyTorch pre-initializer (calls frontend.app)
├── config.py                   # Central hard resource budget caps & usage tracker
├── download_datasets.py        # Safe Kaggle dataset search & budget-gated downloader
├── prepare_dataset.py          # Zip Slip-protected extractor & 63-landmark feature converter
├── train_model.py              # CLI training runner with 60-min cap & 4 GB RAM limiter
├── predict.py                  # Standalone prediction CLI for static images and samples
├── download_translation_model.py # Offline MarianMT English-to-Hindi model downloader
├── requirements.txt            # Dependency manifest with pinned versions
├── README.md                   # Full documentation and Windows 11 setup guide
├── .gitignore                  # Git ignore rules for venv, cache, and recordings
├── frontend/                   # Presentation layer, UI components, pages & styles
│   ├── __init__.py
│   ├── app.py                  # Streamlit application layout & page routing
│   ├── styles/
│   │   ├── __init__.py
│   │   └── theme.py            # Design system, CSS variables, high-contrast dark/light mode
│   ├── components/
│   │   ├── __init__.py
│   │   ├── navbar.py           # Top navigation bar & dark/light theme switch
│   │   ├── footer.py           # Creator credits & global footer
│   │   ├── onboarding.py       # Dismissible first-run 3-step interactive onboarding guide
│   │   ├── telemetry.py        # Hand placement telemetry card & real-time badges
│   │   ├── translation_card.py # Offline Hindi translation card with clipboard integration
│   │   └── sentence_controls.py# Text composition toolbar, size selector & vocalization
│   └── pages/
│       ├── __init__.py
│       ├── home.py             # Hero section, interactive preview & vocabulary coverage
│       ├── how_it_works.py     # 3-step pipeline & ML architecture guide
│       ├── features.py         # Accessibility & assistive tech feature breakdown
│       ├── live_app.py         # Real-time camera feed & posture trainer practice mode
│       ├── studio.py           # Dataset collection studio, alphabet matrix & model trainer
│       └── about.py            # Project mission, tech stack & creator credits
├── backend/                    # ML pipeline, recognition, translation & processing logic
│   ├── __init__.py             # Public backend API exports
│   ├── hand_tracking.py        # MediaPipe Tasks HandLandmarker wrapper & skeleton drawing
│   ├── preprocessing.py        # Wrist-relative translation & scale normalization (63 features)
│   ├── data_collection.py      # Structured CSV dataset manager with session metadata & validation
│   ├── train_model.py          # Random Forest training with group session splitting & metrics
│   ├── predictor.py            # Prediction engine with confidence gating & temporal smoothing
│   ├── text_to_speech.py       # Debounced sentence builder & dual TTS (pyttsx3 + Web Speech API)
│   └── translator.py           # Offline MarianMT neural English-to-Hindi translation
├── src/                        # Backwards-compatibility re-export shims (points to backend.*)
│   ├── __init__.py
│   ├── hand_tracking.py
│   ├── preprocessing.py
│   ├── data_collection.py
│   ├── train_model.py
│   ├── predictor.py
│   ├── text_to_speech.py
│   └── translator.py
├── data/
│   ├── isl_dataset.csv         # Structured dataset with session, participant, and 63 feature columns
│   ├── dataset_manifest.json   # Tracking record of downloaded datasets, licenses, and URLs
│   ├── resource_usage.json     # Persistent audit log of downloaded MB, extracted MB, and API calls
│   ├── raw_datasets/           # Safe download directory for dataset archives
│   └── extracted_datasets/     # Safe path-checked extraction directory
├── models/
│   ├── hand_landmarker.task    # Google MediaPipe HandLandmarker task model
│   ├── isl_classifier.joblib   # Trained Random Forest artifact with metadata and classes
│   ├── training_metrics.json   # Persisted accuracy, precision, recall, F1, and training time log
│   └── opus_mt_en_hi/          # Local MarianMT neural English-to-Hindi offline model weights
├── scripts/
│   └── seed_starter_data.py    # Seed utility for initial baseline ISL dataset
└── tests/
    ├── __init__.py
    ├── conftest.py             # Pytest setup and mock environment fixtures
    ├── test_backend_frontend_refactor.py # Verification of frontend & backend exports & shims
    ├── test_data_validation.py # Dataset integrity, balance, and CSV schema tests
    ├── test_free_budget_enforcement.py # Budget tracker caps and Zip Slip path traversal tests
    ├── test_predictor.py       # Fallback states, smoothing, and sentence builder tests
    ├── test_preprocessing.py   # Invariance, shape, and boundary value tests
    ├── test_theme.py           # Theme CSS, light/dark variables, and creator credits tests
    ├── test_train_model.py     # Resilient model training pipeline tests
    └── test_translation.py     # Offline MarianMT translation, Devanagari output & UI tests
```

---

## 🪟 Windows 11 Step-by-Step Setup Guide

### Step 1: Open PowerShell in Project Directory
Open **PowerShell** (or VS Code / Antigravity integrated terminal) in `d:\vs_code\innotech`:
```powershell
cd d:\vs_code\innotech
```

### Step 2: Create Python Virtual Environment
```powershell
python -m venv .venv
```
*(If `python` points to Microsoft Store, use the full path to Python 3.11: `& "C:\Users\chauh\AppData\Local\Programs\Python\Python311\python.exe" -m venv .venv`)*

### Step 3: Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: (Optional) Re-seed Baseline Dataset or Train Model via CLI
```powershell
python scripts\seed_starter_data.py
python src\train_model.py
```

---

## 🚀 Running the Application

Launch the Streamlit interactive dashboard using either command:
```powershell
# Recommended Windows 11 virtual environment command:
.\.venv\Scripts\python.exe -m streamlit run app.py

# Or if .venv is activated:
python -m streamlit run app.py
```
The browser will automatically open at `http://localhost:8501`.

---

## 🧪 Automated Test Suite & Results

Execute the comprehensive automated test suite covering backend logic, frontend structure, ML invariant pipelines, and offline translation:
```powershell
.\.venv\Scripts\pytest.exe -v
```

### Test Suite Execution Output:
```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\vs_code\innotech
plugins: anyio-4.15.1, platformdirs-4.13.0
collected 39 items


tests/test_backend_frontend_refactor.py::test_backend_exports_and_functionality PASSED [  2%]
tests/test_backend_frontend_refactor.py::test_frontend_exports_and_structure PASSED [  5%]
tests/test_backend_frontend_refactor.py::test_src_backwards_compatibility_shims PASSED [  7%]
tests/test_data_validation.py::test_dataset_initialization PASSED        [ 10%]
tests/test_data_validation.py::test_append_sample PASSED                 [ 13%]
tests/test_data_validation.py::test_invalid_append PASSED                [ 15%]
tests/test_data_validation.py::test_class_counts_and_validation PASSED   [ 18%]
tests/test_data_validation.py::test_delete_samples_for_label PASSED      [ 21%]
tests/test_data_validation.py::test_alphabet_coverage_status PASSED      [ 23%]
tests/test_free_budget_enforcement.py::test_download_budget_enforcement PASSED [ 26%]
tests/test_free_budget_enforcement.py::test_extracted_storage_enforcement PASSED [ 28%]
tests/test_free_budget_enforcement.py::test_kaggle_api_rate_limit_enforcement PASSED [ 31%]
tests/test_free_budget_enforcement.py::test_image_import_limit_enforcement PASSED [ 34%]
tests/test_free_budget_enforcement.py::test_zip_slip_protection PASSED   [ 36%]
tests/test_predictor.py::test_predictor_unloaded_handling PASSED         [ 39%]
tests/test_predictor.py::test_predictor_no_hand_handling PASSED          [ 42%]
tests/test_confidence_threshold_gating PASSED                           [ 44%]
tests/test_predictor.py::test_temporal_smoothing_buffer PASSED           [ 47%]
tests/test_predictor.py::test_sentence_builder_cooldown PASSED           [ 50%]
tests/test_predictor.py::test_sentence_builder_operations PASSED         [ 52%]
tests/test_predictor.py::test_sentence_builder_letters_fingerspelling PASSED [ 55%]
tests/test_predictor.py::test_space_and_clear_requirements PASSED        [ 57%]
tests/test_predictor.py::test_delete_button_requirements PASSED          [ 60%]
tests/test_preprocessing.py::test_feature_names_count PASSED             [ 63%]
tests/test_preprocessing.py::test_normalized_output_shape PASSED         [ 65%]
tests/test_preprocessing.py::test_translation_invariance PASSED          [ 68%]
tests/test_preprocessing.py::test_scale_invariance PASSED                [ 71%]
tests/test_preprocessing.py::test_invalid_input_handling PASSED          [ 73%]
tests/test_preprocessing.py::test_extract_from_landmarks PASSED          [ 76%]
tests/test_theme.py::test_app_theme_css_definitions PASSED               [ 78%]
tests/test_theme.py::test_creator_credits PASSED                         [ 81%]
tests/test_train_model.py::test_model_trainer_pipeline PASSED            [ 84%]
tests/test_train_model.py::test_model_trainer_insufficient_classes PASSED [ 86%]
tests/test_translation.py::test_translator_availability_and_structure PASSED [ 89%]
tests/test_translation.py::test_translator_empty_and_whitespace_input PASSED [ 92%]
tests/test_translation.py::test_translator_missing_directory_handling PASSED [ 94%]
tests/test_translation.py::test_offline_translation_devanagari_sentences PASSED [ 97%]
tests/test_translation.py::test_app_ui_translation_integration PASSED    [100%]

============================= 38 passed in 7.39s ==============================
```

---

## 🌟 Key Features & Accessibility Design

### 1. Live Recognition & Confidence Gating
- Displays instantaneous predictions along with a smoothed majority-vote label (rolling 7 frames) to eliminate high-frequency flickering.
- Transparently alerts `No hand detected` when out of frame, and highlights `Below confidence threshold` when confidence is insufficient.
- Dedicated `➕ Add Current Sign` button for deliberate manual insertion alongside configurable debounced auto-add.

### 2. Sentence Builder with Word Concatenation
- Automatically concatenates individual fingerspelled alphabet letters into complete words (e.g. `C` + `A` + `T` $\to$ `CAT`).
- Converts word gesture underscores (`THANK_YOU`) into clean readable phrases (`THANK YOU`).
- Action toolbar: `Add Sign`, `Insert Space`, `Delete Last Token/Letter`, `Clear All`, and `Copy Text`.

### 3. Dual Speech Output (Local + Browser)
- Local offline speech through Windows SAPI (`pyttsx3`) running in non-blocking background threads.
- Client-side browser synthesis using the HTML5 Web Speech API (`SpeechSynthesisUtterance`), ensuring clear voice output on any browser without audio driver dependencies.

### 4. Studio: A–Z Data Collection & Training
- Complete target selection across all 26 alphabet letters (A–Z) and core word signs.
- Dynamic **ISL Posture Guide** with handshape descriptions, camera positioning tips, and static inflection guidance for movement signs (J and Z).
- Capture controls: Burst mode (10 samples/burst), single-frame capture, and preview.
- Data deletion with explicit confirmation checkbox before removing any samples.
- Live training dashboard with confusion matrix heatmaps and feature evaluation.

### 5. Alphabet Coverage Status (A–Z)
- Real-time dynamic reporting for all 26 letters:
  - **`Active in classifier`**: Included in the currently loaded trained model.
  - **`Ready to train`**: Usable samples exist in `isl_dataset.csv`, ready for model retraining.
  - **`Needs data`**: 0 usable samples recorded yet.
- Direct interactive selector allows jumping straight from coverage matrix to recording in Studio.

---

## ⚠️ Linguistic Grounding: ISL vs. ASL

1. **Authentic Indian Sign Language Context**:
   - Standard Indian Sign Language (codified by ISLRTC) historically employs a two-handed manual alphabet (BANZSL family).
   - In computer vision assistive applications using standard single laptop webcams, single-handed fingerspelling postures are adapted.
   - SignBridge respects this distinction and provides explicit posture guidance for each letter.
2. **Movement-Based Signs (J and Z)**:
   - In fluid signing, J and Z involve tracing trajectories in the air.
   - For static landmark classification, SignBridge instructs signers to hold the distinct key inflection handshape (e.g., pinky upright for J, forward index for Z).

---

## ✅ Verification Checklist

- [x] Python 3.11 virtual environment configured.
- [x] All mutually compatible dependencies installed without conflicts.
- [x] MediaPipe Tasks API integration tested and verified with `hand_landmarker.task`.
- [x] Wrist translation invariance & scale normalization verified.
- [x] Structured dataset collection CSV schema with session metadata verified.
- [x] Random Forest model training pipeline with GroupShuffleSplit / Stratified fallback verified.
- [x] Real-time inference engine with temporal smoothing & confidence gating verified.
- [x] Sentence builder debouncing cooldown, word concatenation, & dual text-to-speech verified.
- [x] A–Z data collection tool with ISL guidance and confirmation deletion implemented.
- [x] Alphabet Coverage Status dynamically driven by dataset CSV and model artifact.
- [x] Offline neural English-to-Hindi translation using local MarianMT (`models/opus_mt_en_hi`).
- [x] Clean modular frontend (`frontend/`) and backend (`backend/`) architecture with backwards-compatible `src/` shims.
- [x] All 39 automated unit tests passing across backend, frontend, models, and translation.

