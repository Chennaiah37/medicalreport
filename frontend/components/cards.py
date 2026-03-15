"""
frontend/components/cards.py
==============================
Reusable HTML card renderers used across all pages.
Each function returns HTML string or calls st.markdown directly.
"""

import re
import streamlit as st
import pandas as pd
from backend.modules.diseases import DISEASE_DB, lookup_disease
from backend.modules.clinicalbert import parse_sections, detect_negations
from .charts import make_confidence_chart


# ── Helpers ───────────────────────────────────────────────────────────────────

def match_badge(c: float) -> tuple:
    if c >= 50: return "Strong match",   "b-g"
    if c >= 25: return "Possible match", "b-y"
    return "Weak match", "b-r"

def bar_color(c: float) -> str:
    if c >= 50: return "#2563eb"
    if c >= 25: return "#f59e0b"
    return "#ef4444"

def highlight_text(text: str, disease: str) -> str:
    info = DISEASE_DB.get(disease, {})
    if not info:
        return text
    sections = parse_sections(text)
    pmh_txt  = " ".join(
        s[1] for s in sections
        if s[0] in ("past medical history", "pmh", "medications", "past history")
    )
    res = text
    for kw in info.get("kws", []):
        p   = re.compile(re.escape(kw), re.IGNORECASE)
        cls = "hh" if kw.lower() in pmh_txt.lower() else "hw"
        res = p.sub(f'<span class="{cls}">{kw}</span>', res)
    return res


# ── Organ icon tile grid (from reference UI) ──────────────────────────────────

ORGAN_TILES = [
    {"label": "Lungs",    "icon": "🫁", "cat": "🫁 Lungs & Breathing"},
    {"label": "Heart",    "icon": "❤️", "cat": "❤️ Heart & Blood"},
    {"label": "Brain",    "icon": "🧠", "cat": "🧠 Brain & Nerves"},
    {"label": "Stomach",  "icon": "🍽️", "cat": "🍽️ Stomach & Digestion"},
    {"label": "Diabetes", "icon": "🩸", "cat": "🩸 Diabetes & Hormones"},
    {"label": "Bones",    "icon": "🦴", "cat": "🦴 Bones & Joints"},
    {"label": "Kidneys",  "icon": "🫘", "cat": "🫘 Kidneys & Urology"},
    {"label": "Mental",   "icon": "🧘", "cat": "🧠 Mental Health"},
    {"label": "Infections","icon":"🦠",  "cat": "🦠 Infections"},
    {"label": "Skin",     "icon": "👁️", "cat": "👁️ Skin & Eyes"},
]

def render_organ_tiles(active_cat: str = "All") -> str:
    """Render the organ icon tile grid — inspired by reference UI."""
    tiles = ""
    for t in ORGAN_TILES:
        active = "active" if t["cat"] == active_cat else ""
        tiles += f"""
        <div class="organ-tile {active}" title="{t['cat']}">
            <span class="organ-icon">{t['icon']}</span>
            <span class="organ-name">{t['label']}</span>
        </div>"""
    return f'<div class="organ-grid">{tiles}</div>'


# ── Disease feature cards (from reference UI) ─────────────────────────────────

def render_disease_feature_card(disease: str, info: dict) -> str:
    """Colorful disease feature card — inspired by reference UI."""
    color    = info.get("color", "#2563eb")
    plain    = info.get("plain", disease).split("(")[0].strip()
    icon     = info.get("icon", "🏥")
    category = info.get("category", "").split("&")[0].strip().lstrip("🫁❤️🧠🍽️🩸🦴🫘🧘🦠👁️").strip()
    icd10    = info.get("icd10", "N/A")

    # Lighten the color for background
    return f"""
    <div class="disease-card" style="background:{color}18;border:1.5px solid {color}44;">
        <div class="dc-label" style="color:{color};">{category}</div>
        <div class="dc-name"  style="color:{color}aa; -webkit-text-fill-color:{color};">{plain}</div>
        <div style="font-size:11px;color:{color}88;margin-top:4px;">ICD-10: {icd10}</div>
        <span class="dc-icon">{icon}</span>
    </div>"""


# ── Hero result card ──────────────────────────────────────────────────────────

def render_hero_card(top_key: str, top_info: dict, top_c: float, engine: str):
    """Render the primary prediction hero card."""
    ml_lbl, ml_cls = match_badge(top_c)
    urg_css = top_info.get("urgency_level", "medium")
    col     = top_info.get("color", "#2563eb")
    cat     = top_info.get("category", "")

    st.markdown(f"""
    <div class="hero" style="border-left-color:{col};">
        <div class="hero-name">{top_info.get("icon","🏥")} {top_info.get("plain", top_key)}</div>
        <div class="hero-med">
            Medical name: {top_key} &nbsp;·&nbsp; ICD-10: {top_info.get("icd10","N/A")}
        </div>
        <div style="margin-top:10px;">
            <span class="badge {ml_cls}">{ml_lbl} · {top_c}%</span>
            <span class="cat-tag" style="background:{col}22;color:{col};">{cat}</span>
        </div>
    </div>
    <div class="urg-{urg_css}">{top_info.get("urgency","See a doctor soon")}</div>
    <div style="font-size:0.78rem;color:#94a3b8;margin-bottom:0.6rem;">
        Engine: {engine}
    </div>
    """, unsafe_allow_html=True)


# ── Result tabs ───────────────────────────────────────────────────────────────

def render_result_tabs(
    top_key: str, top_info: dict, urg_level: str, urgency: str,
    diseases: list, confs: list, signals: list,
    clinical_text: str, top_n: int, hf_status: str
):
    """Render the 6-tab result panel."""
    t1, t2, t3, t4, t5, t6 = st.tabs([
        "💬 What is it?", "💊 Medicines",
        "🩺 Which doctor?", "🏠 At home",
        "🔬 Signals", "📊 All results"
    ])
    urg_css = top_info.get("urgency_level", "medium")

    with t1:
        st.markdown('<div class="sec-t">What this condition means</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="what-box">{top_info.get("what","")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-t">Symptoms found in your report</div>', unsafe_allow_html=True)
        chips = "".join(f'<span class="chip">✅ {s}</span>' for s in top_info.get("symptoms", []))
        st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-t">Key words highlighted</div>', unsafe_allow_html=True)
        st.markdown("🟡 Yellow = active symptom &nbsp;|&nbsp; 🟠 Orange = past history")
        hl = highlight_text(clinical_text[:800], top_key)
        st.markdown(
            f'<div class="info-box" style="font-size:0.85rem;line-height:1.75;">'
            f'{hl}{"..." if len(clinical_text) > 800 else ""}</div>',
            unsafe_allow_html=True
        )

    with t2:
        st.markdown('<div class="sec-t">Medicines your doctor might suggest</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">Common medicines — your doctor decides what is right for you.</div>', unsafe_allow_html=True)
        for name, desc in top_info.get("meds", []):
            st.markdown(
                f'<div class="med-card"><div class="cn">💊 {name}</div>'
                f'<div class="cd">{desc}</div></div>',
                unsafe_allow_html=True
            )

    with t3:
        st.markdown('<div class="sec-t">Which type of doctor to see</div>', unsafe_allow_html=True)
        for name, desc in top_info.get("specs", []):
            st.markdown(
                f'<div class="spec-card"><div class="cn">🩺 {name}</div>'
                f'<div class="cd">{desc}</div></div>',
                unsafe_allow_html=True
            )
        st.markdown('<div class="sec-t">When to go</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="urg-{urg_css}">{top_info.get("urgency","")}</div>', unsafe_allow_html=True)

    with t4:
        st.markdown('<div class="sec-t">What you can do at home</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">These do not replace medicine but help alongside treatment.</div>', unsafe_allow_html=True)
        for tip in top_info.get("tips", []):
            st.markdown(f'<div class="tip-card">✅ {tip}</div>', unsafe_allow_html=True)

    with t5:
        st.markdown('<div class="sec-t">Clinical signals detected</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="urg-{urg_level}">{urgency}</div>', unsafe_allow_html=True)
        render_signal_cards(signals)
        st.markdown(
            f'<div style="font-size:0.75rem;color:#94a3b8;">BioClinicalBERT status: <b>{hf_status}</b></div>',
            unsafe_allow_html=True
        )

    with t6:
        st.markdown('<div class="sec-t">All conditions — ranked by match strength</div>', unsafe_allow_html=True)
        rows = []
        for rank, (d, c) in enumerate(zip(diseases[:top_n], confs[:top_n]), 1):
            _, dinfo  = lookup_disease(d)
            lbl, _    = match_badge(c)
            col2      = dinfo.get("color", "#2563eb")
            bc        = bar_color(c)
            st.markdown(f"""
            <div class="pred-row">
                <span class="pred-rnk" style="background:{col2};">#{rank}</span>
                <div style="flex:1;min-width:0;">
                    <div class="pred-pn">{dinfo.get("icon","🏥")} {dinfo.get("plain",d)}</div>
                    <div class="pred-mn">{d} · ICD-10: {dinfo.get("icd10","N/A")} · {dinfo.get("category","")}</div>
                    <div class="bar-bg"><div class="bar-fg" style="width:{c}%;background:{bc};"></div></div>
                    <div style="font-size:0.78rem;color:#64748b;">{c}% — {lbl}</div>
                </div>
            </div>""", unsafe_allow_html=True)
            rows.append({
                "Condition": dinfo.get("plain", d), "Medical name": d,
                "Match %": c, "ICD-10": dinfo.get("icd10", "N/A"),
                "Category": dinfo.get("category", ""), "Urgency": dinfo.get("urgency", "")
            })

        st.markdown("<br>", unsafe_allow_html=True)
        st.pyplot(make_confidence_chart(diseases[:top_n], confs[:top_n]), use_container_width=True)
        st.download_button(
            "⬇️ Save results as CSV",
            pd.DataFrame(rows).to_csv(index=False),
            "medreport_results.csv", "text/csv"
        )


# ── Signal cards ──────────────────────────────────────────────────────────────

def render_signal_cards(signals: list):
    if not signals:
        st.info("No specific clinical signals detected.")
        return
    for s in signals:
        border = "#ef4444" if s["severity"] == 4 else "#f59e0b" if s["severity"] == 3 else "#86efac"
        st.markdown(
            f'<div class="sig-card" style="border-left:4px solid {border};">'
            f'<b>{s["category"]}</b> — {s["priority"]}<br>'
            f'<span style="font-size:0.82rem;color:#475569;">Keywords: {", ".join(s["matched"])}</span><br>'
            f'<span style="font-size:0.82rem;color:#64748b;">{s["advice"]}</span></div>',
            unsafe_allow_html=True
        )


# ── Empty waiting state ───────────────────────────────────────────────────────

def render_empty_state():
    st.markdown("""
    <div class="empty-state">
        <div class="es-icon">📋</div>
        <div class="es-title">Waiting for your report</div>
        <div class="es-sub">Add a report on the left then click Analyse</div>
    </div>
    """, unsafe_allow_html=True)
