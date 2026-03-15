"""
frontend/pages/check_report.py
================================
Page 1 — Check My Report
Handles all 5 input methods + runs prediction + renders results.
"""

import os
import streamlit as st

from backend.modules.predictor  import run_prediction
from backend.modules.dataloader import load_dataset, extract_pdf, load_txt, get_sample_notes
from backend.modules.logger     import save_log
from backend.modules.diseases   import DISEASE_DB

from frontend.components.cards  import (
    render_hero_card, render_result_tabs,
    render_signal_cards, render_empty_state,
    render_organ_tiles,
)


def render(use_bert: bool, top_n: int):
    """Render the full Check My Report page."""

    # Header
    st.markdown("""
    <div class="app-hdr">
        <h1>🏥 MedReport AI</h1>
        <p>BioClinicalBERT + 51 diseases across 10 categories — every input gives output</p>
    </div>
    """, unsafe_allow_html=True)

    # Organ icon tile navigation (from reference UI)
    st.markdown('<div class="sec-t">Browse by body system</div>', unsafe_allow_html=True)
    st.markdown(render_organ_tiles(), unsafe_allow_html=True)

    # Engine status badge
    token_ok = bool(os.environ.get("HF_TOKEN", "")) and len(os.environ.get("HF_TOKEN", "")) > 10
    if use_bert and token_ok:
        st.markdown('<span class="engine-on">🟢 BioClinicalBERT (HuggingFace) + Built-in NLP — Active</span>', unsafe_allow_html=True)
    elif use_bert:
        st.markdown('<span class="engine-off">🟠 Paste HuggingFace token in sidebar to enable BioClinicalBERT</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="engine-off">⚙️ Built-in Clinical NLP — Active (always works without token)</span>', unsafe_allow_html=True)
    st.markdown("")

    left, right = st.columns([1, 1], gap="large")

    # ── INPUT PANEL ──────────────────────────────────────────────────────────
    with left:
        st.markdown('<div class="sec-t">Step 1 — Add your report</div>', unsafe_allow_html=True)
        method = st.radio(
            "Input method",
            ["📋 Paste text", "📄 Upload PDF", "📝 Upload TXT", "🗂️ From Dataset", "💡 Use an example"],
            horizontal=True
        )
        clinical_text = ""

        if "Paste" in method:
            clinical_text = st.text_area(
                "Paste the report here:", height=270,
                placeholder="Paste any doctor's note, discharge summary, clinic report, or symptom description..."
            )

        elif "PDF" in method:
            uploaded = st.file_uploader("Choose a PDF file", type=["pdf"])
            if uploaded:
                with st.spinner("Reading PDF..."):
                    clinical_text = extract_pdf(uploaded)
                st.success(f"✅ PDF extracted — {len(clinical_text)} characters")
                with st.expander("👁️ Preview extracted text"):
                    st.write(clinical_text[:1500] + ("..." if len(clinical_text) > 1500 else ""))

        elif "TXT" in method:
            uploaded = st.file_uploader("Choose a text file", type=["txt"])
            if uploaded:
                clinical_text = load_txt(uploaded)
                st.success(f"✅ File loaded — {len(clinical_text)} characters")

        elif "Dataset" in method:
            df_data = load_dataset()
            if df_data.empty:
                st.warning("clinical_notes.csv not found in backend/data/")
            else:
                st.success(f"Dataset loaded — {len(df_data)} patient records")
                search = st.text_input("Search records", "")
                filt = df_data[
                    df_data["disease"].str.contains(search, case=False, na=False) |
                    df_data["clinical_note"].str.contains(search, case=False, na=False)
                ] if search else df_data
                opts = [
                    f"{r.patient_id} — {r.disease} ({r.age}y, {r.gender})"
                    for _, r in filt.iterrows()
                ]
                if opts:
                    sel = st.selectbox("Select a patient record:", opts)
                    pid = sel.split(" — ")[0]
                    row = df_data[df_data["patient_id"] == pid].iloc[0]
                    clinical_text = row["clinical_note"]
                    st.info(
                        f"**Patient:** {row.patient_id} | **Age:** {row.age} | "
                        f"**Gender:** {row.gender} | **Known diagnosis:** {row.disease}"
                    )

        elif "example" in method:
            examples = get_sample_notes()
            choice   = st.selectbox("Choose an example:", list(examples.keys()))
            clinical_text = examples[choice]
            st.info("✅ Example loaded — click Analyse Report below")

        st.markdown("<br>", unsafe_allow_html=True)
        go = st.button("🔍  Analyse Report", type="primary", use_container_width=True)

    # ── RESULTS PANEL ─────────────────────────────────────────────────────────
    with right:
        st.markdown('<div class="sec-t">Step 2 — Results</div>', unsafe_allow_html=True)

        if not go:
            render_empty_state()

        elif not clinical_text.strip():
            st.warning("Please add a report first.")

        else:
            with st.spinner("Analysing your report..."):
                result = run_prediction(text=clinical_text, use_hf=use_bert)

            diseases    = result["diseases"]
            confs       = result["confidences"]
            engine      = result["engine"]
            signals     = result["signals"]
            urgency     = result["urgency"]
            urg_level   = result["urgency_level"]
            hf_status   = result["hf_status"]
            top_key     = result["top_key"]
            top_info    = result["top_info"]

            if not diseases:
                st.warning("No specific disease matched. Showing clinical signals detected:")
                render_signal_cards(signals)
                st.markdown(f'<div class="urg-{urg_level}">{urgency}</div>', unsafe_allow_html=True)
            else:
                # Log the prediction
                save_log(clinical_text, top_key, confs[0], engine)

                # Hero card
                render_hero_card(top_key, top_info, confs[0], engine)

                # 6-tab results
                render_result_tabs(
                    top_key=top_key, top_info=top_info,
                    urg_level=urg_level, urgency=urgency,
                    diseases=diseases, confs=confs,
                    signals=signals, clinical_text=clinical_text,
                    top_n=top_n, hf_status=hf_status
                )
