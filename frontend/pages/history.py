"""
frontend/pages/history.py
===========================
Page 4 — My History
History table rendered with white text on dark background.
"""

import streamlit as st
import pandas as pd
from backend.modules.logger import load_log


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

    st.markdown('<div class="page-title">📋 My Report History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Every report you have analysed is saved here automatically</div>',
        unsafe_allow_html=True,
    )

    logs = load_log()

    if not logs:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">📋</div>
            <div class="es-title">No history yet</div>
            <div class="es-sub">Go to Check My Report and analyse a report to see it here</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Build dataframe ───────────────────────────────────────────────────────
    df_log = pd.DataFrame(logs)
    df_log["timestamp"] = (
        pd.to_datetime(df_log["timestamp"]).dt.strftime("%d %b %Y  %H:%M")
    )
    df_log = df_log.rename(columns={
        "timestamp":  "Date & Time",
        "prediction": "Condition Found",
        "confidence": "Match %",
        "engine":     "Engine Used",
        "snippet":    "Report Snippet",
    })

    # ── Metrics ───────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.metric("Total analyses",    len(df_log))
    c2.metric("Unique conditions", df_log["Condition Found"].nunique())
    c3.metric(
        "Engines used",
        df_log["Engine Used"].nunique() if "Engine Used" in df_log.columns else 1,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Show newest first ─────────────────────────────────────────────────────
    display = df_log[::-1].reset_index(drop=True)

    # Keep only columns that exist
    show_cols = [c for c in ["Date & Time", "Condition Found", "Match %", "Engine Used", "Report Snippet"] if c in display.columns]
    display   = display[show_cols]

    st.markdown(
        f'<div class="showing-text"><b style="color:#e2e8f0;">{len(display)}</b> predictions recorded</div>',
        unsafe_allow_html=True,
    )

    col_config = {
        "Date & Time":     st.column_config.TextColumn("Date & Time",    width="medium"),
        "Condition Found": st.column_config.TextColumn("Condition",      width="medium"),
        "Match %":         st.column_config.NumberColumn("Match %",      width="small", format="%.1f%%"),
        "Engine Used":     st.column_config.TextColumn("Engine",         width="medium"),
        "Report Snippet":  st.column_config.TextColumn("Report Snippet", width="large"),
    }

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={k: v for k, v in col_config.items() if k in show_cols},
    )

    # ── Download ──────────────────────────────────────────────────────────────
    st.download_button(
        "⬇️ Download history as CSV",
        df_log.to_csv(index=False),
        "medreport_history.csv",
        "text/csv",
    )
