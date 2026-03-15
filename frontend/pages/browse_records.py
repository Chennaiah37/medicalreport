"""
frontend/pages/browse_records.py
==================================
Page 3 — Browse Patient Records
Dataset table rendered with white text on dark background.
"""

import streamlit as st
import pandas as pd
from backend.modules.dataloader import load_dataset
from frontend.components.charts import make_distribution_chart


# ── Inline dark-table CSS injected only on this page ─────────────────────────
_TABLE_CSS = """
<style>
/* Force white text in ALL dataframe elements */
[data-testid="stDataFrame"] *                       { color: #ffffff !important; }
[data-testid="stDataFrame"] [role="columnheader"]   { color: #60a5fa !important; background: #0d1f35 !important; font-weight: 700 !important; }
[data-testid="stDataFrame"] [role="gridcell"]       { color: #ffffff !important; background: #0f1624 !important; }
[data-testid="stDataFrame"] [role="row"]:nth-child(even) [role="gridcell"] { background: #111827 !important; }
[data-testid="stDataFrame"] [role="row"]:hover [role="gridcell"]           { background: #142035 !important; }
.showing-text { color: #94b8d8 !important; font-size: 0.88rem; margin-bottom: 0.5rem; }
</style>
"""


def render():
    st.markdown(_TABLE_CSS, unsafe_allow_html=True)

    st.markdown('<div class="page-title">📂 Browse Patient Records</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Explore the sample dataset — 20 patient records across 8 conditions</div>',
        unsafe_allow_html=True,
    )

    df = load_dataset()
    if df.empty:
        st.error("clinical_notes.csv not found. Make sure it is in backend/data/")
        return

    # ── Stats row ─────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-num">{len(df)}</div>'
            f'<div class="stat-lbl">Total Records</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-num">{df["disease"].nunique()}</div>'
            f'<div class="stat-lbl">Conditions Covered</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="stat-card"><div class="stat-num">{round(df["age"].mean(), 1)}</div>'
            f'<div class="stat-lbl">Average Age</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.pyplot(make_distribution_chart(df), use_container_width=True)
    st.markdown("---")

    # ── Filters ───────────────────────────────────────────────────────────────
    cf1, cf2, cf3 = st.columns(3)
    with cf1:
        disease_f = st.multiselect(
            "Filter by condition", sorted(df["disease"].unique()), default=[]
        )
    with cf2:
        gender_f = st.multiselect(
            "Filter by gender", sorted(df["gender"].unique()), default=[]
        )
    with cf3:
        search = st.text_input("🔎 Search keyword", "")

    filtered = df.copy()
    if disease_f:
        filtered = filtered[filtered["disease"].isin(disease_f)]
    if gender_f:
        filtered = filtered[filtered["gender"].isin(gender_f)]
    if search:
        filtered = filtered[
            filtered["disease"].str.contains(search, case=False, na=False) |
            filtered["clinical_note"].str.contains(search, case=False, na=False)
        ]

    # ── Table with white text ─────────────────────────────────────────────────
    st.markdown(
        f'<div class="showing-text">Showing <b style="color:#e2e8f0;">{len(filtered)}</b> '
        f'of <b style="color:#e2e8f0;">{len(df)}</b> records</div>',
        unsafe_allow_html=True,
    )

    display_df = filtered[["patient_id", "age", "gender", "disease", "clinical_note"]].copy()
    display_df.columns = ["Patient ID", "Age", "Gender", "Disease / Condition", "Clinical Note"]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=380,
        column_config={
            "Patient ID":          st.column_config.TextColumn("Patient ID",       width="small"),
            "Age":                 st.column_config.NumberColumn("Age",            width="small"),
            "Gender":              st.column_config.TextColumn("Gender",           width="small"),
            "Disease / Condition": st.column_config.TextColumn("Disease",         width="medium"),
            "Clinical Note":       st.column_config.TextColumn("Clinical Note",   width="large"),
        },
    )

    st.download_button(
        "⬇️ Download as CSV",
        filtered.to_csv(index=False),
        "records.csv",
        "text/csv",
    )
