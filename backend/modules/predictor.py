"""
backend/modules/predictor.py
==============================
Prediction orchestrator — calls clinicalbert engine,
returns a structured result dict used by all frontend pages.
"""

import os
from .clinicalbert import analyze_report
from .diseases     import DISEASE_DB, lookup_disease


def run_prediction(text: str, use_hf: bool = False) -> dict:
    """
    Main prediction entry point called by frontend pages.

    Args:
        text   : raw clinical note text
        use_hf : whether to call BioClinicalBERT via HuggingFace API

    Returns:
        {
          diseases      : list[str]   — matched disease names
          confidences   : list[float] — percentage scores
          engine        : str         — engine description
          hf_status     : str         — HuggingFace API status
          signals       : list[dict]  — clinical signal categories
          urgency       : str         — plain-English urgency message
          urgency_level : str         — critical / high / medium / low / none
          top_info      : dict        — full info for #1 disease
          top_key       : str         — matched DB key for #1 disease
        }
    """
    if not text or not text.strip():
        return _empty_result("no_input")

    result = analyze_report(
        text       = text,
        disease_db = DISEASE_DB,
        use_hf     = use_hf
    )

    # Enrich with full disease info for the top prediction
    top_key, top_info = ("", {})
    if result["diseases"]:
        top_key, top_info = lookup_disease(result["diseases"][0])

    result["top_key"]  = top_key
    result["top_info"] = top_info
    return result


def enrich_predictions(diseases: list, confidences: list) -> list:
    """
    Zip disease names + confidences with their full DB info.
    Returns list of dicts ready for the frontend to render.
    """
    rows = []
    for d, c in zip(diseases, confidences):
        key, info = lookup_disease(d)
        rows.append({
            "key":        key,
            "plain":      info.get("plain", d),
            "icon":       info.get("icon", "🏥"),
            "color":      info.get("color", "#2563eb"),
            "category":   info.get("category", ""),
            "icd10":      info.get("icd10", "N/A"),
            "urgency":    info.get("urgency", ""),
            "urgency_level": info.get("urgency_level", "medium"),
            "confidence": c,
            "info":       info,
        })
    return rows


def _empty_result(reason: str) -> dict:
    return {
        "diseases":      [],
        "confidences":   [],
        "engine":        "none",
        "hf_status":     reason,
        "signals":       [],
        "urgency":       "No input provided.",
        "urgency_level": "none",
        "top_key":       "",
        "top_info":      {},
    }
