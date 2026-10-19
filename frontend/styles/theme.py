"""
Theme definitions and dynamic CSS generation for SignBridge.
Supports dark/light themes, anti-stale overlays, and accessible styling.
"""
def get_theme_css(theme: str) -> str:
    """Generate dynamic CSS tokens and Streamlit component overrides based on theme."""
    is_dark = (theme == "dark")
    if is_dark:
        vars_css = """
        --sb-bg: #0c0d10;
        --sb-surface: #14161b;
        --sb-surface-muted: #1b1e25;
        --sb-surface-highlight: #242832;
        --sb-border: #232731;
        --sb-border-subtle: #1b1e25;
        --sb-border-strong: #353b49;
        --sb-text-main: #f4f5f8;
        --sb-text-muted: #9ea3ae;
        --sb-text-subtle: #6e7380;
        --sb-primary: #6366f1;
        --sb-primary-hover: #818cf8;
        --sb-primary-light: rgba(99, 102, 241, 0.15);
        --sb-primary-border: rgba(99, 102, 241, 0.35);
        --sb-success: #2dd4bf;
        --sb-success-bg: rgba(45, 212, 191, 0.12);
        --sb-success-border: rgba(45, 212, 191, 0.30);
        --sb-warning: #fbbf24;
        --sb-warning-bg: rgba(251, 191, 36, 0.12);
        --sb-warning-border: rgba(251, 191, 36, 0.30);
        --sb-radius-card: 8px;
        --sb-radius-btn: 6px;
        --sb-radius-badge: 5px;
        --sb-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.4);
        --sb-shadow-md: 0 4px 8px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -2px rgba(0, 0, 0, 0.4);
        --sb-shadow-lg: 0 12px 20px -3px rgba(0, 0, 0, 0.6);
        """
    else:
        vars_css = """
        --sb-bg: #fbfaf8;
        --sb-surface: #ffffff;
        --sb-surface-muted: #f3f2ee;
        --sb-surface-highlight: #edebe6;
        --sb-border: #e8e6df;
        --sb-border-subtle: #f0eee8;
        --sb-border-strong: #d1cec4;
        --sb-text-main: #141517;
        --sb-text-muted: #50535a;
        --sb-text-subtle: #757982;
        --sb-primary: #4338ca;
        --sb-primary-hover: #3730a3;
        --sb-primary-light: #eef2ff;
        --sb-primary-border: #c7d2fe;
        --sb-success: #0f766e;
        --sb-success-bg: #f0fdfa;
        --sb-success-border: #99f6e4;
        --sb-warning: #b45309;
        --sb-warning-bg: #fffbeb;
        --sb-warning-border: #fde68a;
        --sb-radius-card: 8px;
        --sb-radius-btn: 6px;
        --sb-radius-badge: 5px;
        --sb-shadow: 0 1px 2px 0 rgba(16, 24, 40, 0.05);
        --sb-shadow-md: 0 4px 6px -1px rgba(16, 24, 40, 0.08), 0 2px 4px -2px rgba(16, 24, 40, 0.05);
        --sb-shadow-lg: 0 10px 15px -3px rgba(16, 24, 40, 0.08), 0 4px 6px -4px rgba(16, 24, 40, 0.04);
        """

    return f"""
    <style>
    /* Google Fonts: Inter & JetBrains Mono */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {{
        {vars_css}
    }}

    /* Global Application Canvas */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    section.main,
    .main,
    [data-testid="stMainBlockContainer"],
    [data-testid="stBottomBlockContainer"] {{
        background-color: var(--sb-bg) !important;
        color: var(--sb-text-main) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        letter-spacing: -0.011em;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* Main Container Constraints */
    .block-container,
    [data-testid="stMainBlockContainer"] {{
        padding-top: 1.25rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1180px !important;
        background-color: var(--sb-bg) !important;
    }}

    /* Anti-Stale interaction rules: CRITICAL FOR CAMERA LOOPS */
    div[data-stale="true"],
    .stApp [data-stale="true"],
    [data-testid="stAppViewContainer"] [data-stale="true"],
    [data-testid="stElementContainer"][data-stale="true"],
    [data-testid="stMainBlockContainer"][data-stale="true"] {{
        opacity: 1 !important;
        filter: none !important;
        pointer-events: auto !important;
        transition: none !important;
    }}
    .stButton > button {{
        pointer-events: auto !important;
    }}

    /* Streamlit Global Typography Overrides */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--sb-text-main) !important;
    }}
    p, span, label, div[data-testid="stMarkdownContainer"] p {{
        color: inherit;
    }}
    div[data-testid="stCaptionContainer"] p {{
        color: var(--sb-text-muted) !important;
    }}

    /* Global Button Base Styling */
    .stButton > button,
    div[data-testid="stButton"] > button,
    div[class*="st-key-"] > button {{
        border-radius: var(--sb-radius-btn) !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.95rem !important;
        transition: all 0.15s ease !important;
        letter-spacing: -0.01em !important;
    }}

    /* Primary Buttons */
    button[kind="primary"],
    button[data-testid="baseButton-primary"],
    div.stButton > button[kind="primary"],
    div[data-testid="stButton"] > button[kind="primary"] {{
        background-color: var(--sb-primary) !important;
        border: 1px solid var(--sb-primary) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px 0 rgba(67, 56, 202, 0.25) !important;
    }}
    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stButton"] > button[kind="primary"]:hover {{
        background-color: var(--sb-primary-hover) !important;
        border-color: var(--sb-primary-hover) !important;
        color: #ffffff !important;
    }}

    /* Secondary Buttons */
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"],
    div.stButton > button[kind="secondary"],
    div[data-testid="stButton"] > button[kind="secondary"] {{
        background-color: var(--sb-surface) !important;
        border: 1px solid var(--sb-border) !important;
        color: var(--sb-text-main) !important;
        box-shadow: var(--sb-shadow) !important;
    }}
    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    div.stButton > button[kind="secondary"]:hover,
    div[data-testid="stButton"] > button[kind="secondary"]:hover {{
        background-color: var(--sb-surface-muted) !important;
        border-color: var(--sb-border-strong) !important;
        color: var(--sb-text-main) !important;
    }}

    /* Streamlit Form Inputs & Controls */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] {{
        background-color: var(--sb-surface) !important;
        border: 1px solid var(--sb-border) !important;
        border-radius: var(--sb-radius-btn) !important;
        color: var(--sb-text-main) !important;
    }}
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    div[data-baseweb="textarea"] textarea {{
        color: var(--sb-text-main) !important;
        background-color: transparent !important;
    }}
    div[data-baseweb="popover"],
    ul[role="listbox"] {{
        background-color: var(--sb-surface) !important;
        border: 1px solid var(--sb-border) !important;
        box-shadow: var(--sb-shadow-md) !important;
    }}
    li[role="option"] {{
        background-color: var(--sb-surface) !important;
        color: var(--sb-text-main) !important;
    }}
    li[role="option"]:hover,
    li[aria-selected="true"] {{
        background-color: var(--sb-surface-muted) !important;
        color: var(--sb-text-main) !important;
    }}
    div[data-testid="stCheckbox"] label,
    div[data-testid="stRadio"] label {{
        color: var(--sb-text-main) !important;
    }}
    div[data-testid="stSlider"] label {{
        color: var(--sb-text-main) !important;
    }}

    /* Metrics & Cards */
    div[data-testid="stMetric"] {{
        background-color: var(--sb-surface) !important;
        border: 1px solid var(--sb-border) !important;
        border-radius: var(--sb-radius-card) !important;
        padding: 0.85rem 1rem !important;
        box-shadow: var(--sb-shadow) !important;
    }}
    div[data-testid="stMetricLabel"] p {{
        color: var(--sb-text-muted) !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: var(--sb-text-main) !important;
    }}

    /* Clean Expander */
    [data-testid="stExpander"] {{
        background-color: var(--sb-surface) !important;
        border: 1px solid var(--sb-border) !important;
        border-radius: var(--sb-radius-card) !important;
        box-shadow: var(--sb-shadow) !important;
    }}
    [data-testid="stExpander"] summary {{
        color: var(--sb-text-main) !important;
    }}
    [data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {{
        color: var(--sb-text-muted) !important;
    }}

    /* Top Brand Navigation Header */
    .sb-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1.25rem;
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: var(--sb-radius-card);
        margin-bottom: 0.6rem;
        box-shadow: var(--sb-shadow);
    }}
    .sb-brand {{
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }}
    .sb-brand-logo {{
        width: 28px;
        height: 28px;
        background: var(--sb-primary);
        color: #ffffff;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
        box-shadow: 0 1px 3px rgba(67, 56, 202, 0.3);
    }}
    .sb-brand-name {{
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--sb-text-main);
        letter-spacing: -0.025em;
    }}
    .sb-brand-badge {{
        font-size: 0.68rem;
        font-weight: 600;
        color: var(--sb-primary);
        background: var(--sb-primary-light);
        border: 1px solid var(--sb-primary-border);
        padding: 0.12rem 0.45rem;
        border-radius: var(--sb-radius-badge);
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}
    .sb-nav-tagline {{
        font-size: 0.82rem;
        color: var(--sb-text-subtle);
        font-weight: 400;
    }}

    /* Navigation Row Link / Button Styling */
    .st-key-nav_home button,
    .st-key-nav_how button,
    .st-key-nav_feat button,
    .st-key-nav_practice button,
    .st-key-nav_studio button,
    .st-key-nav_about button,
    div[class*="st-key-nav_"]:not([class*="st-key-nav_launch"]) button {{
        border-radius: var(--sb-radius-btn) !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.75rem !important;
        transition: all 0.15s ease !important;
        border: 1px solid transparent !important;
        background-color: transparent !important;
        color: var(--sb-text-muted) !important;
        box-shadow: none !important;
    }}
    .st-key-nav_home button:hover,
    .st-key-nav_how button:hover,
    .st-key-nav_feat button:hover,
    .st-key-nav_practice button:hover,
    .st-key-nav_studio button:hover,
    .st-key-nav_about button:hover,
    div[class*="st-key-nav_"]:not([class*="st-key-nav_launch"]) button:hover {{
        background-color: var(--sb-surface-muted) !important;
        color: var(--sb-text-main) !important;
        border-color: var(--sb-border) !important;
    }}
    .st-key-nav_home button[kind="primary"],
    .st-key-nav_how button[kind="primary"],
    .st-key-nav_feat button[kind="primary"],
    .st-key-nav_practice button[kind="primary"],
    .st-key-nav_studio button[kind="primary"],
    .st-key-nav_about button[kind="primary"],
    .st-key-nav_home button[data-testid="baseButton-primary"],
    .st-key-nav_how button[data-testid="baseButton-primary"],
    .st-key-nav_feat button[data-testid="baseButton-primary"],
    .st-key-nav_practice button[data-testid="baseButton-primary"],
    .st-key-nav_studio button[data-testid="baseButton-primary"],
    .st-key-nav_about button[data-testid="baseButton-primary"],
    div[class*="st-key-nav_"]:not([class*="st-key-nav_launch"]) button[kind="primary"],
    div[class*="st-key-nav_"]:not([class*="st-key-nav_launch"]) button[data-testid="baseButton-primary"] {{
        background-color: var(--sb-surface) !important;
        color: var(--sb-primary) !important;
        font-weight: 600 !important;
        border: 1px solid var(--sb-border) !important;
        box-shadow: var(--sb-shadow) !important;
    }}
    .st-key-nav_launch button,
    div[class*="st-key-nav_launch"] button {{
        background-color: var(--sb-primary-light) !important;
        color: var(--sb-primary) !important;
        font-weight: 600 !important;
        border: 1px solid var(--sb-primary-border) !important;
    }}
    .st-key-nav_launch button:hover,
    div[class*="st-key-nav_launch"] button:hover {{
        background-color: var(--sb-primary) !important;
        color: #ffffff !important;
        border-color: var(--sb-primary) !important;
    }}
    .st-key-nav_launch button[kind="primary"],
    .st-key-nav_launch button[data-testid="baseButton-primary"],
    div[class*="st-key-nav_launch"] button[kind="primary"],
    div[class*="st-key-nav_launch"] button[data-testid="baseButton-primary"] {{
        background-color: var(--sb-primary) !important;
        color: #ffffff !important;
        border: 1px solid var(--sb-primary-hover) !important;
        box-shadow: 0 1px 3px rgba(67, 56, 202, 0.25) !important;
    }}

    /* Theme Switcher Button */
    .st-key-theme_toggle_btn button,
    div[class*="st-key-theme_toggle_btn"] button {{
        background-color: var(--sb-surface) !important;
        border: 1px solid var(--sb-border) !important;
        color: var(--sb-text-main) !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.8rem !important;
        box-shadow: var(--sb-shadow) !important;
    }}
    .st-key-theme_toggle_btn button:hover,
    div[class*="st-key-theme_toggle_btn"] button:hover {{
        background-color: var(--sb-surface-muted) !important;
        border-color: var(--sb-border-strong) !important;
    }}

    /* Live Workspace Interactive Buttons */
    .st-key-live_space button,
    .st-key-live_del button,
    .st-key-live_clear button {{
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
    }}
    .st-key-live_del button:hover {{
        color: #ef4444 !important;
        border-color: rgba(239, 68, 68, 0.4) !important;
        background-color: rgba(239, 68, 68, 0.06) !important;
    }}
    .st-key-live_clear button:hover {{
        color: #ef4444 !important;
        border-color: rgba(239, 68, 68, 0.4) !important;
        background-color: rgba(239, 68, 68, 0.06) !important;
    }}
    .st-key-live_translate_btn button {{
        background-color: var(--sb-primary-light) !important;
        color: var(--sb-primary) !important;
        font-weight: 600 !important;
        border: 1px solid var(--sb-primary-border) !important;
    }}
    .st-key-live_translate_btn button:hover {{
        background-color: var(--sb-primary) !important;
        color: #ffffff !important;
        border-color: var(--sb-primary) !important;
    }}

    /* Hero Section */
    .sb-hero-tag {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--sb-primary);
        background: var(--sb-primary-light);
        border: 1px solid var(--sb-primary-border);
        padding: 0.2rem 0.55rem;
        border-radius: var(--sb-radius-badge);
        margin-bottom: 1.1rem;
    }}
    .sb-hero-title {{
        font-size: 3.1rem;
        font-weight: 800;
        line-height: 1.12;
        color: var(--sb-text-main);
        letter-spacing: -0.035em;
        margin-bottom: 1.1rem;
    }}
    .sb-hero-sub {{
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.6;
        color: var(--sb-text-muted);
        margin-bottom: 1.75rem;
        max-width: 530px;
    }}
    .sb-hero-notice {{
        margin-top: 1.75rem;
        font-size: 0.8rem;
        color: var(--sb-text-subtle);
        line-height: 1.5;
        border-left: 2px solid var(--sb-border);
        padding-left: 0.75rem;
    }}

    /* Product Preview Window */
    .sb-preview-window {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: var(--sb-radius-card);
        overflow: hidden;
        box-shadow: var(--sb-shadow-md);
    }}
    .sb-preview-header {{
        background: var(--sb-surface-muted);
        border-bottom: 1px solid var(--sb-border);
        padding: 0.55rem 0.9rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.75rem;
        color: var(--sb-text-subtle);
        font-family: 'JetBrains Mono', monospace;
    }}
    .sb-preview-dots {{
        display: flex;
        gap: 5px;
    }}
    .sb-dot {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--sb-border-strong);
    }}
    .sb-preview-body {{
        padding: 1rem;
    }}
    .sb-preview-screen {{
        background: #111317;
        border-radius: 6px;
        height: 230px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .sb-preview-overlay {{
        position: absolute;
        top: 10px;
        left: 10px;
        background: rgba(20, 22, 27, 0.85);
        color: #e4e4e7;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 4px;
        padding: 3px 7px;
        font-size: 0.68rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.02em;
    }}
    .sb-preview-pill {{
        background: var(--sb-success);
        color: #ffffff;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        padding: 4px 10px;
        border-radius: 4px;
        letter-spacing: 0.06em;
        margin-top: 8px;
    }}
    .sb-preview-footer {{
        margin-top: 0.85rem;
        padding: 0.75rem 0.9rem;
        background: var(--sb-surface-muted);
        border: 1px solid var(--sb-border);
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        color: var(--sb-text-main);
    }}

    /* Section Headings */
    .sb-section-tag {{
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--sb-primary);
        margin-bottom: 0.35rem;
    }}
    .sb-section-heading {{
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--sb-text-main);
        letter-spacing: -0.025em;
        margin-bottom: 0.5rem;
    }}
    .sb-section-desc {{
        font-size: 0.98rem;
        color: var(--sb-text-muted);
        line-height: 1.55;
        margin-bottom: 1.75rem;
        max-width: 660px;
    }}

    /* Feature & Step Cards */
    .sb-step-card {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: var(--sb-radius-card);
        padding: 1.35rem 1.25rem;
        height: 100%;
        box-shadow: var(--sb-shadow);
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    .sb-step-card:hover {{
        border-color: var(--sb-border-strong);
        box-shadow: var(--sb-shadow-md);
    }}
    .sb-step-num {{
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--sb-primary);
        margin-bottom: 0.6rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.06em;
    }}
    .sb-step-title {{
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--sb-text-main);
        margin-bottom: 0.45rem;
        letter-spacing: -0.015em;
    }}
    .sb-step-text {{
        font-size: 0.88rem;
        color: var(--sb-text-muted);
        line-height: 1.55;
    }}

    /* Live Recognition Elements */
    .sb-sentence-output {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: var(--sb-radius-card);
        padding: 1.1rem 1.25rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.25rem;
        line-height: 1.55;
        min-height: 96px;
        color: var(--sb-text-main);
        word-break: break-word;
        white-space: pre-wrap;
        margin-bottom: 0.75rem;
        box-shadow: var(--sb-shadow);
    }}
    .sb-translation-container {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-left: 3px solid var(--sb-primary);
        border-radius: var(--sb-radius-card);
        padding: 0.95rem 1.2rem;
        margin-top: 0.4rem;
        margin-bottom: 0.85rem;
        box-shadow: var(--sb-shadow);
    }}
    .sb-translation-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
    }}
    .sb-translation-badge {{
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--sb-primary);
        background: var(--sb-primary-light);
        border: 1px solid var(--sb-primary-border);
        padding: 0.15rem 0.5rem;
        border-radius: var(--sb-radius-badge);
        letter-spacing: 0.04em;
    }}
    .sb-translation-output {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        line-height: 1.5;
        color: var(--sb-text-main);
        word-break: break-word;
        white-space: pre-wrap;
    }}
    .sb-badge-detected {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 1.05rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        padding: 0.4rem 0.9rem;
        border-radius: var(--sb-radius-badge);
        letter-spacing: -0.01em;
        margin-top: 0.5rem;
        margin-bottom: 0.35rem;
    }}
    .sb-badge-success {{
        background: var(--sb-success-bg);
        color: var(--sb-success);
        border: 1px solid var(--sb-success-border);
    }}
    .sb-badge-neutral {{
        background: var(--sb-surface-muted);
        color: var(--sb-text-muted);
        border: 1px solid var(--sb-border);
    }}
    .sb-badge-warning {{
        background: var(--sb-warning-bg);
        color: var(--sb-warning);
        border: 1px solid var(--sb-warning-border);
    }}

    .sb-cam-offline {{
        background: #111317;
        border: 1px solid var(--sb-border);
        border-radius: var(--sb-radius-card);
        height: 380px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #94a3b8;
        text-align: center;
        padding: 1.5rem;
    }}

    /* Info & Callout Cards */
    .sb-callout {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: var(--sb-radius-card);
        padding: 1.25rem;
        box-shadow: var(--sb-shadow);
    }}
    .sb-callout-title {{
        font-weight: 600;
        font-size: 0.92rem;
        color: var(--sb-text-main);
        margin-bottom: 0.35rem;
    }}
    .sb-callout-text {{
        font-size: 0.86rem;
        color: var(--sb-text-muted);
        line-height: 1.55;
    }}

    /* Alphabet Matrix Cell */
    .sb-matrix-cell {{
        margin-bottom: 6px;
        text-align: center;
        padding: 7px 4px;
        border-radius: 5px;
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        box-shadow: var(--sb-shadow);
    }}
    .sb-matrix-letter {{
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--sb-text-main);
        font-family: 'JetBrains Mono', monospace;
    }}
    .sb-matrix-badge-active {{
        color: var(--sb-success);
        font-weight: 600;
        font-size: 0.68rem;
        background: var(--sb-success-bg);
        padding: 1px 5px;
        border-radius: 3px;
        border: 1px solid var(--sb-success-border);
        display: inline-block;
    }}
    .sb-matrix-badge-ready {{
        color: var(--sb-warning);
        font-weight: 600;
        font-size: 0.68rem;
        background: var(--sb-warning-bg);
        padding: 1px 5px;
        border-radius: 3px;
        border: 1px solid var(--sb-warning-border);
        display: inline-block;
    }}
    .sb-matrix-badge-needs {{
        color: var(--sb-text-subtle);
        font-size: 0.68rem;
        background: var(--sb-surface-muted);
        padding: 1px 5px;
        border-radius: 3px;
        border: 1px solid var(--sb-border);
        display: inline-block;
    }}

    /* Clean Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        border-bottom: 1px solid var(--sb-border);
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 44px;
        border-radius: 6px 6px 0 0;
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--sb-text-muted);
        background-color: transparent;
        border: none;
        padding: 0 1.1rem;
    }}
    .stTabs [aria-selected="true"] {{
        color: var(--sb-primary) !important;
        font-weight: 600 !important;
        border-bottom: 2px solid var(--sb-primary) !important;
    }}

    /* Interactive Onboarding Card */
    .sb-onboarding-card {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-left: 4px solid var(--sb-primary);
        border-radius: var(--sb-radius-card);
        padding: 1.15rem 1.35rem;
        margin-bottom: 1.35rem;
        box-shadow: var(--sb-shadow);
    }}
    .sb-onboarding-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }}
    .sb-onboarding-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 0.85rem;
        margin-bottom: 1rem;
    }}
    .sb-onboarding-step {{
        background: var(--sb-surface-muted);
        border: 1px solid var(--sb-border-subtle);
        border-radius: 6px;
        padding: 0.85rem;
    }}
    .sb-onboarding-step-num {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--sb-primary);
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }}
    .sb-onboarding-step-title {{
        font-weight: 600;
        font-size: 0.88rem;
        color: var(--sb-text-main);
        margin-bottom: 0.35rem;
    }}
    .sb-onboarding-step-desc {{
        font-size: 0.8rem;
        color: var(--sb-text-muted);
        line-height: 1.45;
    }}

    /* Interactive Demo Banner */
    .sb-demo-banner {{
        background: var(--sb-warning-bg);
        border: 1px solid var(--sb-warning-border);
        border-radius: var(--sb-radius-card);
        padding: 0.75rem 1.1rem;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }}
    .sb-demo-badge {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--sb-warning);
        background: rgba(245, 158, 11, 0.15);
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.04em;
    }}

    /* Recognition History Item */
    .sb-history-chip {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 6px;
        padding: 0.3rem 0.6rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        margin: 0.2rem;
        box-shadow: var(--sb-shadow);
    }}
    .sb-history-sign {{
        font-weight: 700;
        color: var(--sb-primary);
    }}
    .sb-history-meta {{
        font-size: 0.7rem;
        color: var(--sb-text-subtle);
    }}

    /* Practice Mode Card */
    .sb-practice-card {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: var(--sb-radius-card);
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.25rem;
        box-shadow: var(--sb-shadow);
    }}
    .sb-practice-target {{
        font-size: 2.2rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        color: var(--sb-primary);
        line-height: 1;
    }}

    /* Pulse Flash on Added Sign */
    .sb-added-pulse {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        color: var(--sb-success);
        background: var(--sb-success-bg);
        border: 1px solid var(--sb-success-border);
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
    }}

    /* Footer */
    .sb-footer {{
        margin-top: 4.5rem;
        padding-top: 2rem;
        border-top: 1px solid var(--sb-border);
        color: var(--sb-text-subtle);
        font-size: 0.84rem;
    }}
    .sb-footer-brand {{
        font-weight: 700;
        color: var(--sb-text-main);
        font-size: 0.95rem;
        margin-bottom: 0.35rem;
    }}
    .sb-footer-col-title {{
        font-weight: 600;
        color: var(--sb-text-main);
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.45rem;
    }}
    .sb-footer-text {{
        color: var(--sb-text-muted);
        line-height: 1.5;
        font-size: 0.82rem;
    }}

    /* STRICT: Camera & Image Color Integrity (DO NOT INVERT OR FILTER) */
    [data-testid="stImage"] img,
    img {{
        filter: none !important;
    }}
    </style>
    """
