"""
frontend/components/sidebar.py
================================
Sidebar rendering — navigation, token input, settings.
Returns (page, use_bert, top_n).
"""

import os
import streamlit as st
from backend.modules.diseases import DISEASE_DB


def render_sidebar() -> tuple:
    """Render sidebar and return (page, use_bert, top_n)."""
    with st.sidebar:
        st.markdown("## 🏥 MedReport AI")
        st.markdown("---")

        page = st.radio(
            "",
            [
                "🔍 Check My Report",
                "📊 Disease Guide",
                "📂 Browse Records",
                "📋 My History",
                "❓ How It Works",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        # BioClinicalBERT token
        hf_token = st.text_input(
            "🔑 HuggingFace Token (optional)",
            value=os.environ.get("HF_TOKEN", ""),
            type="password",
            help="Paste your HF_TOKEN to enable BioClinicalBERT enrichment.",
        )
        if hf_token:
            os.environ["HF_TOKEN"] = hf_token
            try:
                import backend.modules.clinicalbert as _cb
                _cb.HF_TOKEN = hf_token
                _cb.HEADERS  = {"Authorization": f"Bearer {hf_token}"}
            except Exception:
                pass

        use_bert = st.toggle(
            "🤖 Use BioClinicalBERT",
            value=bool(hf_token),
            help="ON = Bio_ClinicalBERT via HuggingFace API. OFF = Built-in NLP (always works).",
        )

        top_n = st.slider("Results to show", 1, 5, 3)

        st.markdown("---")
        st.markdown(
            f'<p style="font-size:0.74rem;color:#94a3b8;">'
            f"v7.0 · {len(DISEASE_DB)} diseases · 10 categories</p>",
            unsafe_allow_html=True,
        )

    return page, use_bert, top_n
