"""
frontend/components/styles.py
================================
MedReport AI — Dark Theme
Deep navy background, bright accents, high contrast text.
Every component clearly visible in dark mode.
"""

import streamlit as st


def inject_css():
    """Call once at app startup to inject all global dark-theme styles."""
    st.markdown(_CSS, unsafe_allow_html=True)


_CSS = """
<style>

/* ══════════════════════════════════════════════════════════
   BASE — deep dark background everywhere
   ══════════════════════════════════════════════════════════ */
html, body,
section[data-testid="stMain"],
div[data-testid="stAppViewContainer"],
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
div.main, div.block-container {
    background-color: #0d1117 !important;
    color: #e2e8f0 !important;
}
div.block-container {
    padding: 1.4rem 2rem !important;
    max-width: 1300px !important;
}

/* All generic text defaults */
p, span, div, h1, h2, h3, h4, li {
    color: #e2e8f0;
}

/* ══════════════════════════════════════════════════════════
   SIDEBAR
   ══════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #0d1f35 0%, #060e1a 100%) !important;
    border-right: 1px solid #1e3554 !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div  { color: #94b8d8 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3   { color: #e2eaf4 !important; }
section[data-testid="stSidebar"] hr   { border-color: #1e3554 !important; }
/* Radio options */
section[data-testid="stSidebar"] .stRadio label span { color: #c8daf0 !important; }

/* ══════════════════════════════════════════════════════════
   FORM INPUTS
   ══════════════════════════════════════════════════════════ */
textarea, input[type="text"], input[type="password"] {
    background: #161d2e !important;
    color: #e2e8f0 !important;
    border: 1.5px solid #2a3f5f !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
}
textarea:focus, input[type="text"]:focus, input[type="password"]:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
}
label,
.stTextArea label,
.stRadio label,
.stSlider label,
.stFileUploader label,
.stSelectbox label { color: #94b8d8 !important; }

/* Select / dropdown */
div[data-baseweb="select"] > div {
    background: #161d2e !important;
    border-color: #2a3f5f !important;
    color: #e2e8f0 !important;
}
div[data-baseweb="popover"] { background: #161d2e !important; }
div[data-baseweb="menu"]    { background: #161d2e !important; }
li[role="option"]           { background: #161d2e !important; color: #e2e8f0 !important; }
li[role="option"]:hover     { background: #1e2d45 !important; }

/* File uploader */
div[data-testid="stFileUploader"] {
    background: #161d2e !important;
    border: 1.5px dashed #2a3f5f !important;
    border-radius: 10px !important;
}

/* ══════════════════════════════════════════════════════════
   BUTTONS
   ══════════════════════════════════════════════════════════ */
div.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.4) !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.5) !important;
}
div.stDownloadButton > button {
    background: #0d2a1a !important;
    color: #4ade80 !important;
    border: 1.5px solid #166534 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* ══════════════════════════════════════════════════════════
   TABS
   ══════════════════════════════════════════════════════════ */
div[data-baseweb="tab-list"] {
    background: #161d2e !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #1e3554 !important;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
button[data-baseweb="tab"]:hover {
    color: #93c5fd !important;
    background: #1e2d45 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: #1e3a5e !important;
    color: #60a5fa !important;
    font-weight: 700 !important;
}
div[data-baseweb="tab-panel"] {
    background: #0f1624 !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1.2rem !important;
    border: 1px solid #1e3554 !important;
    border-top: none !important;
}

/* ══════════════════════════════════════════════════════════
   EXPANDER
   ══════════════════════════════════════════════════════════ */
div[data-testid="stExpander"] {
    background: #0f1624 !important;
    border: 1px solid #1e3554 !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary p {
    color: #93c5fd !important;
}

/* ══════════════════════════════════════════════════════════
   METRICS
   ══════════════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: #0f1624 !important;
    border-radius: 10px !important;
    padding: 0.8rem !important;
    border: 1px solid #1e3554 !important;
}
[data-testid="stMetric"] label      { color: #64748b !important; }
[data-testid="stMetricValue"]        { color: #60a5fa !important; }

/* ══════════════════════════════════════════════════════════
   DATAFRAME — white text, dark background
   ══════════════════════════════════════════════════════════ */
[data-testid="stDataFrame"] { background: #0f1624 !important; border-radius: 10px !important; }

/* iframe that wraps the table */
[data-testid="stDataFrame"] iframe { background: #0f1624 !important; }

/* All text inside dataframe */
[data-testid="stDataFrame"] *,
[data-testid="stDataFrame"] div,
[data-testid="stDataFrame"] span,
[data-testid="stDataFrame"] p    { color: #ffffff !important; }

/* Header row */
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] [role="columnheader"],
[data-testid="stDataFrame"] [role="columnheader"] * {
    background: #0d1f35 !important;
    color: #60a5fa !important;
    font-weight: 700 !important;
    border-bottom: 1px solid #1e3554 !important;
}

/* Data cells */
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] [role="gridcell"],
[data-testid="stDataFrame"] [role="gridcell"] * {
    background: #0f1624 !important;
    color: #ffffff !important;
    border-bottom: 1px solid #1a2540 !important;
}

/* Alternating row */
[data-testid="stDataFrame"] tr:nth-child(even) td,
[data-testid="stDataFrame"] tr:nth-child(even) [role="gridcell"] {
    background: #111827 !important;
}

/* Hover row */
[data-testid="stDataFrame"] tr:hover td,
[data-testid="stDataFrame"] tr:hover [role="gridcell"] {
    background: #142035 !important;
}

/* Scrollbar inside dataframe */
[data-testid="stDataFrame"] ::-webkit-scrollbar       { background: #0d1117; }
[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb { background: #1e3554; }

/* Success / info / warning / error alerts */
div[data-testid="stAlert"] { border-radius: 10px !important; }
div.stSuccess { background: #0a2018 !important; color: #4ade80 !important; border-color: #166534 !important; }
div.stInfo    { background: #0c1e35 !important; color: #93c5fd !important; border-color: #1e3a5e !important; }
div.stWarning { background: #1c1500 !important; color: #fbbf24 !important; border-color: #78350f !important; }
div.stError   { background: #1a0909 !important; color: #f87171 !important; border-color: #7f1d1d !important; }

/* Spinner text */
div[data-testid="stSpinner"] p { color: #93c5fd !important; }

/* Slider */
div[data-testid="stSlider"] div[role="slider"] {
    background: #3b82f6 !important;
}

/* Toggle */
div[data-testid="stToggle"] span { background: #1e3554 !important; }

/* ══════════════════════════════════════════════════════════
   SCROLLBAR
   ══════════════════════════════════════════════════════════ */
::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #1e3554; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2a4a6e; }


/* ══════════════════════════════════════════════════════════
   CUSTOM HTML COMPONENTS — DARK
   ══════════════════════════════════════════════════════════ */

/* App Header */
.app-hdr {
    background: linear-gradient(135deg, #0d1f35 0%, #1a3a6e 50%, #0d1f35 100%);
    border: 1px solid #1e3a6e;
    padding: 1.8rem 2rem;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 1.4rem;
}
.app-hdr h1 { color: #e2eaf4; font-size: 1.9rem; margin: 0 0 0.3rem; }
.app-hdr p  { color: #60a5fa; font-size: 0.95rem; margin: 0; }

/* Disclaimer */
.disc {
    background: #1c1206;
    border-left: 4px solid #f59e0b;
    padding: 0.75rem 1.1rem;
    border-radius: 0 10px 10px 0;
    font-size: 0.87rem;
    color: #fbbf24;
    margin-bottom: 1.2rem;
}

/* Organ Icon Tiles */
.organ-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0,1fr));
    gap: 10px;
    margin: 0.8rem 0 1.2rem;
}
.organ-tile {
    background: #0f1624;
    border: 1px solid #1e3554;
    border-radius: 14px;
    padding: 12px 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s;
}
.organ-tile:hover {
    border-color: #3b82f6;
    background: #142035;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59,130,246,0.2);
}
.organ-tile.active {
    border: 2px solid #3b82f6;
    background: #142035;
}
.organ-icon { font-size: 26px; display: block; margin-bottom: 5px; }
.organ-name { font-size: 11px; color: #64748b; font-weight: 500; }

/* Disease Feature Cards */
.disease-card {
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 0.6rem;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.15s;
    border: 1px solid rgba(255,255,255,0.08);
}
.disease-card:hover { transform: translateY(-2px); }
.disease-card .dc-label {
    font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.07em;
    margin-bottom: 4px; opacity: 0.7;
}
.disease-card .dc-name { font-size: 1.1rem; font-weight: 800; line-height: 1.25; }
.disease-card .dc-icon { font-size: 2rem; position: absolute; right: 14px; top: 14px; opacity: 0.2; }

/* Hero Result Card */
.hero {
    background: #0f1624;
    border-radius: 16px;
    border: 1px solid #1e3554;
    border-left: 6px solid #3b82f6;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.8rem;
}
.hero-name { font-size: 1.4rem; font-weight: 800; color: #e2eaf4; margin: 0 0 3px; }
.hero-med  { font-size: 0.82rem; color: #475569; }

/* Urgency strips */
.urg-critical, .urg-high {
    background: #1a0909;
    border: 1.5px solid #7f1d1d;
    color: #fca5a5;
    padding: 0.7rem 1rem; border-radius: 10px;
    font-weight: 700; font-size: 0.9rem; margin-bottom: 0.7rem;
}
.urg-medium {
    background: #1c1200;
    border: 1.5px solid #78350f;
    color: #fbbf24;
    padding: 0.7rem 1rem; border-radius: 10px;
    font-weight: 700; font-size: 0.9rem; margin-bottom: 0.7rem;
}
.urg-low, .urg-none {
    background: #062010;
    border: 1.5px solid #166534;
    color: #4ade80;
    padding: 0.7rem 1rem; border-radius: 10px;
    font-weight: 700; font-size: 0.9rem; margin-bottom: 0.7rem;
}

/* Badges */
.badge {
    display: inline-block; padding: 4px 12px;
    border-radius: 20px; font-size: 0.8rem;
    font-weight: 700; margin: 4px 4px 0 0;
}
.b-g    { background: #062010; color: #4ade80; border: 1px solid #166534; }
.b-y    { background: #1c1200; color: #fbbf24; border: 1px solid #78350f; }
.b-r    { background: #1a0909; color: #f87171; border: 1px solid #7f1d1d; }
.b-b    { background: #0c1e35; color: #60a5fa; border: 1px solid #1e3a6e; }
.b-gray { background: #0f1624; color: #64748b; border: 1px solid #1e3554; }

/* Section title */
.sec-t {
    font-size: 0.72rem; font-weight: 800;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: #3b82f6; margin: 1rem 0 0.6rem;
    padding-bottom: 0.4rem; border-bottom: 1px solid #1e3554;
}

/* What-is box */
.what-box {
    background: #0c1e35;
    border-left: 4px solid #3b82f6;
    padding: 1rem 1.2rem;
    border-radius: 0 10px 10px 0;
    font-size: 0.93rem; color: #93c5fd; line-height: 1.7; margin-bottom: 0.8rem;
}

/* Info box */
.info-box {
    background: #0f1624;
    border: 1px solid #1e3554;
    border-radius: 10px; padding: 0.8rem 1rem;
    font-size: 0.87rem; color: #94b8d8; margin-bottom: 0.5rem;
}

/* Symptom chips */
.chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.4rem 0 0.8rem; }
.chip {
    background: #0c1e35; color: #60a5fa;
    padding: 4px 13px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 600; border: 1px solid #1e3a6e;
}

/* Medicine cards */
.med-card {
    background: #071a0f;
    border: 1px solid #166534;
    border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.55rem;
}
.med-card .cn { font-size: 0.92rem; font-weight: 700; color: #4ade80; }
.med-card .cd { font-size: 0.84rem; color: #86efac; margin-top: 3px; line-height: 1.5; }

/* Specialist cards */
.spec-card {
    background: #0c1e35;
    border: 1px solid #1e3a6e;
    border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.55rem;
}
.spec-card .cn { font-size: 0.92rem; font-weight: 700; color: #60a5fa; }
.spec-card .cd { font-size: 0.84rem; color: #93c5fd; margin-top: 3px; }

/* Tip cards */
.tip-card {
    background: #1a1100;
    border: 1px solid #78350f;
    border-radius: 10px; padding: 0.7rem 1rem;
    margin-bottom: 0.45rem; font-size: 0.87rem; color: #fbbf24;
}

/* Signal cards */
.sig-card {
    border-radius: 10px; padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    background: #0f1624; border: 1px solid #1e3554;
    color: #e2e8f0;
}
.sig-card b { color: #60a5fa; }
.sig-card span { color: #94b8d8 !important; }

/* Prediction rows */
.pred-row {
    background: #0f1624;
    border: 1px solid #1e3554;
    border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 10px;
}
.pred-rnk {
    display: inline-block; width: 26px; height: 26px;
    border-radius: 50%; font-size: 0.75rem; font-weight: 800;
    text-align: center; line-height: 26px; color: #fff; flex-shrink: 0;
}
.pred-pn { font-size: 0.95rem; font-weight: 700; color: #e2eaf4; }
.pred-mn { font-size: 0.78rem; color: #475569; }
.bar-bg  { background: #1e3554; border-radius: 6px; height: 8px; margin: 5px 0 2px; overflow: hidden; }
.bar-fg  { height: 100%; border-radius: 6px; }

/* Highlights */
.hw { background: #3a2e00; padding: 1px 5px; border-radius: 4px; font-weight: 700; color: #fbbf24; }
.hh { background: #3a1a00; padding: 1px 5px; border-radius: 4px; font-style: italic; color: #fb923c; }

/* Stat cards */
.stat-card {
    background: #0f1624;
    border: 1px solid #1e3554;
    border-radius: 12px; padding: 1.1rem; text-align: center;
}
.stat-num { font-size: 1.9rem; font-weight: 800; color: #60a5fa; }
.stat-lbl { font-size: 0.8rem; color: #475569; margin-top: 2px; }

/* How It Works steps */
.step-box {
    background: #0f1624;
    border: 1px solid #1e3554;
    border-radius: 14px; padding: 1rem 1.3rem; margin-bottom: 0.7rem;
}
.step-n {
    display: inline-block; background: #2563eb; color: #ffffff;
    width: 26px; height: 26px; border-radius: 50%;
    text-align: center; line-height: 26px;
    font-size: 0.78rem; font-weight: 800; margin-right: 8px;
}
.step-t { font-size: 0.95rem; font-weight: 700; color: #e2eaf4; }
.step-b { font-size: 0.87rem; color: #64748b; margin-top: 5px; line-height: 1.55; }

/* Engine badges */
.engine-on {
    background: #062010; color: #4ade80;
    border: 1px solid #166534;
    padding: 5px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 700;
}
.engine-off {
    background: #1a0e00; color: #fb923c;
    border: 1px solid #7c3a00;
    padding: 5px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 700;
}

/* Category tag */
.cat-tag {
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: 0.78rem; font-weight: 700; margin-right: 6px;
}

/* Page headers */
.page-title { font-size: 1.5rem; font-weight: 800; color: #e2eaf4; margin-bottom: 0.2rem; }
.page-sub   { font-size: 0.9rem; color: #475569; margin-bottom: 1.1rem; }

/* Empty state */
.empty-state {
    background: #0f1624;
    border: 2px dashed #1e3554;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    margin-top: 0.5rem;
}
.empty-state .es-icon  { font-size: 3rem; margin-bottom: 0.8rem; }
.empty-state .es-title { font-size: 1rem; font-weight: 700; color: #93c5fd; margin-bottom: 0.4rem; }
.empty-state .es-sub   { font-size: 0.87rem; color: #475569; }

/* Code block */
pre, code {
    background: #0d1117 !important;
    color: #7dd3fc !important;
    border: 1px solid #1e3554 !important;
    border-radius: 8px !important;
}

</style>
"""
