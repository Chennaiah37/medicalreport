"""
frontend/pages/how_it_works.py
================================
Page 5 — How It Works
Plain-English explanation of the app pipeline.
"""

import streamlit as st
from backend.modules.diseases import DISEASE_DB


STEPS = [
    (
        "You upload or paste your report",
        "Give the app a doctor's note, discharge summary or clinic report — "
        "as PDF, text file, or simply paste it in.",
    ),
    (
        "Bio_ClinicalBERT reads the medical language",
        "If a HuggingFace token is provided, the app calls "
        "emilyalsentzer/Bio_ClinicalBERT via the HuggingFace Inference API. "
        "Without a token, the built-in clinical NLP engine runs — it always gives output.",
    ),
    (
        "Clinical sections are weighted differently",
        "Words in Chief Complaint and HPI get 3× weight. "
        "Past Medical History gets 0.4× — so old conditions don't dominate results.",
    ),
    (
        "Negation detection removes false signals",
        "Phrases like 'denies cough', 'no fever', 'absence of wheeze' are detected "
        "and removed from scoring automatically.",
    ),
    (
        f"Matched against {len(DISEASE_DB)} diseases across 10 categories",
        "Covers Lungs, Heart, Brain, Stomach, Diabetes, Bones, Kidneys, "
        "Mental Health, Infections and Skin & Eyes.",
    ),
    (
        "Results explained in plain English",
        "Every disease is explained simply — what it means, what the medicines do, "
        "which doctor to see, and what you can do at home.",
    ),
]


def render():
    st.markdown('<div class="page-title">❓ How Does This App Work?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Everything explained simply — no medical knowledge needed</div>',
        unsafe_allow_html=True,
    )

    for i, (title, body) in enumerate(STEPS, 1):
        st.markdown(
            f'<div class="step-box">'
            f'<span class="step-n">{i}</span>'
            f'<span class="step-t">{title}</span>'
            f'<div class="step-b">{body}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### BioClinicalBERT setup (optional)")
    st.code(
        "# Get a free token from huggingface.co/settings/tokens\n"
        "# Option 1: Paste it in the sidebar token field\n"
        "# Option 2: Set an environment variable\n"
        "set HF_TOKEN=hf_your_token_here       # Windows\n"
        "export HF_TOKEN=hf_your_token_here    # Mac / Linux",
        language="bash",
    )

    st.markdown(
        f'<div class="what-box">'
        f"⚠️ <b>Remember:</b> This app is a learning and research tool only — "
        f"not a medical diagnosis. Always visit a qualified doctor for any health concern.<br><br>"
        f"<b>Diseases covered:</b> {len(DISEASE_DB)} conditions across 10 body system categories."
        f"</div>",
        unsafe_allow_html=True,
    )
