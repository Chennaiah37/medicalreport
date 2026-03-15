"""
MedReport AI v7.0
==================
Entry point — run with:  streamlit run app.py

Project structure
-----------------
app.py                          ← this file (entry point only)
backend/
  modules/
    diseases.py                 ← 51-disease knowledge base
    clinicalbert.py             ← BioClinicalBERT + built-in NLP engine
    predictor.py                ← prediction orchestrator
    logger.py                   ← audit logging
    dataloader.py               ← CSV, PDF, TXT loading + sample notes
  data/
    clinical_notes.csv          ← sample patient dataset
  results/
    audit_log.json              ← auto-generated prediction history
frontend/
  components/
    styles.py                   ← all CSS in one place
    sidebar.py                  ← sidebar navigation + settings
    charts.py                   ← matplotlib chart builders
    cards.py                    ← reusable HTML card renderers
  pages/
    check_report.py             ← Page 1: upload + predict + results
    disease_guide.py            ← Page 2: colorful disease card guide
    browse_records.py           ← Page 3: dataset explorer
    history.py                  ← Page 4: audit log viewer
    how_it_works.py             ← Page 5: plain-English pipeline explainer
"""

import sys
import os

# Make sure backend and frontend are importable from app root
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

# ── Page config (must be the very first Streamlit call) ──────────────────────
st.set_page_config(
    page_title="MedReport AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS ────────────────────────────────────────────────────────────────
from frontend.components.styles import inject_css
inject_css()

# ── Disclaimer (shown on every page) ─────────────────────────────────────────
st.markdown("""
<div class="disc">
⚠️ <b>Important:</b> This is a <b>learning and research tool only</b> — not a real medical diagnosis.
Always see a qualified doctor for health concerns.
In an emergency call your local emergency number immediately.
</div>
""", unsafe_allow_html=True)

# ── Sidebar (returns nav choice + settings) ───────────────────────────────────
from frontend.components.sidebar import render_sidebar
page, use_bert, top_n = render_sidebar()

# ── Route to correct page ─────────────────────────────────────────────────────
if "🔍 Check My Report" in page:
    from frontend.pages.check_report import render
    render(use_bert=use_bert, top_n=top_n)

elif "📊 Disease Guide" in page:
    from frontend.pages.disease_guide import render
    render()

elif "📂 Browse Records" in page:
    from frontend.pages.browse_records import render
    render()

elif "📋 My History" in page:
    from frontend.pages.history import render
    render()

elif "❓ How It Works" in page:
    from frontend.pages.how_it_works import render
    render()
