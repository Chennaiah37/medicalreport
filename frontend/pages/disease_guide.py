"""
frontend/pages/disease_guide.py
================================
Page 2 — Disease Guide
Shows all 51 diseases as colorful feature cards (from reference UI)
with category filtering via organ icon tiles.
"""

import streamlit as st
from backend.modules.diseases import DISEASE_DB, ALL_CATEGORIES
from frontend.components.cards import render_disease_feature_card, render_organ_tiles


def render():
    st.markdown('<div class="page-title">📊 Disease Guide</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-sub">All {len(DISEASE_DB)} diseases — click a body system to filter</div>',
        unsafe_allow_html=True
    )

    # Search bar
    search = st.text_input("🔍 Search diseases", "", placeholder="e.g. diabetes, migraine, skin rash...")

    # Category filter — organ tiles + dropdown
    col_tiles, col_drop = st.columns([3, 1])
    with col_drop:
        cats   = ["All categories"] + list(ALL_CATEGORIES.keys())
        cat_f  = st.selectbox("Filter by category:", cats, label_visibility="collapsed")

    st.markdown('<div class="sec-t">Conditions</div>', unsafe_allow_html=True)

    # Show as 2-column colorful disease cards
    filtered = {
        k: v for k, v in DISEASE_DB.items()
        if (cat_f == "All categories" or v.get("category", "") == cat_f)
        and (not search or search.lower() in k.lower() or search.lower() in v.get("plain", "").lower())
    }

    if not filtered:
        st.info("No diseases found matching your search.")
        return

    items  = list(filtered.items())
    col1, col2 = st.columns(2, gap="small")

    for i, (disease, info) in enumerate(items):
        col = col1 if i % 2 == 0 else col2
        with col:
            card_html = render_disease_feature_card(disease, info)
            with st.expander(
                f'{info.get("icon","🏥")} {info.get("plain", disease).split("(")[0].strip()}  —  {info.get("icd10","N/A")}',
                expanded=False
            ):
                st.markdown(card_html, unsafe_allow_html=True)
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f'<div class="what-box">{info.get("what","")}</div>', unsafe_allow_html=True)
                    st.markdown("**Symptoms:**")
                    for s in info.get("symptoms", []):
                        st.markdown(f"✅ {s}")
                with c2:
                    st.markdown(f"**Category:** {info.get('category','')}")
                    st.markdown(f"**ICD-10:** `{info.get('icd10','N/A')}`")
                    st.markdown(f"**Urgency:** {info.get('urgency','')}")
                    st.markdown("**Specialists:**")
                    for n, _ in info.get("specs", []):
                        st.markdown(f"🩺 {n}")
                    st.markdown("**Medicines:**")
                    for n, _ in info.get("meds", []):
                        st.markdown(f"💊 {n}")
