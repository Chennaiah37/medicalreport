"""
frontend/components/charts.py
================================
All matplotlib chart builders — kept separate from page logic.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from backend.modules.diseases import DISEASE_DB, lookup_disease


def make_confidence_chart(diseases: list, confs: list):
    """Horizontal bar chart of top-N disease confidence scores."""
    labels = [lookup_disease(d)[1].get("plain", d).split("(")[0].strip() for d in diseases]
    colors = [lookup_disease(d)[1].get("color", "#2563eb") for d in diseases]

    fig, ax = plt.subplots(figsize=(7, max(2.5, len(diseases) * 0.9)))
    fig.patch.set_facecolor("#0f1624")
    ax.set_facecolor("#0d1117")

    bars = ax.barh(labels[::-1], confs[::-1], color=colors[::-1], edgecolor="white", height=0.55)
    for bar, c in zip(bars, confs[::-1]):
        ax.text(
            bar.get_width() + 0.6, bar.get_y() + bar.get_height() / 2,
            f"{c}%", va="center", ha="left", fontsize=10,
            fontweight="bold", color="#1e293b"
        )

    ax.set_xlabel("Match strength (%)", color="#64748b", fontsize=10)
    ax.set_xlim(0, 118)
    ax.set_title("All conditions found", fontsize=11, fontweight="bold", color="#93c5fd", pad=8)
    for sp in ax.spines.values():
        sp.set_color("#1e3554")
    ax.tick_params(colors="#64748b")
    plt.tight_layout()
    return fig


def make_distribution_chart(df):
    """Horizontal bar chart of disease distribution in the dataset."""
    counts     = df["disease"].value_counts()
    all_colors = [v.get("color", "#2563eb") for v in DISEASE_DB.values()]
    colors     = [all_colors[i % len(all_colors)] for i in range(len(counts))]

    fig, ax = plt.subplots(figsize=(9, max(4, len(counts) * 0.5)))
    fig.patch.set_facecolor("#0f1624")
    ax.set_facecolor("#0d1117")

    ax.barh(counts.index[::-1], counts.values[::-1], color=colors[::-1], edgecolor="white", height=0.6)
    ax.set_xlabel("Number of records", color="#64748b", fontsize=10)
    ax.set_title("Disease distribution in dataset", fontsize=12, fontweight="bold", color="#93c5fd", pad=8)

    for sp in ax.spines.values():
        sp.set_color("#1e3554")
    ax.tick_params(colors="#64748b")
    plt.tight_layout()
    return fig
