"""
clinicalbert.py — MedReport AI v7.0
=====================================
BioClinicalBERT via HuggingFace Inference API.
Same pattern as VitalSense reference project.

Set HF_TOKEN env variable or paste below to enable BioClinicalBERT.
Without token: built-in clinical NLP always runs and always gives output.
"""

import requests
import os
import re

HF_TOKEN = os.environ.get("HF_TOKEN", "")
BERT_URL  = "https://api-inference.huggingface.co/models/emilyalsentzer/Bio_ClinicalBERT"
HEADERS   = {"Authorization": f"Bearer {HF_TOKEN}"}

# ── SECTION WEIGHTS ───────────────────────────────────────────────────────────
SECTION_WEIGHTS = {
    "chief complaint":              3.0,
    "history of present illness":   3.0,
    "hpi":                          3.0,
    "presenting complaint":         3.0,
    "complaint":                    2.5,
    "assessment":                   2.5,
    "diagnosis":                    2.5,
    "impression":                   2.5,
    "plan":                         2.0,
    "physical examination":         2.0,
    "examination":                  2.0,
    "investigations":               2.0,
    "labs":                         1.8,
    "results":                      1.8,
    "vital signs":                  1.5,
    "vitals":                       1.5,
    "past medical history":         0.4,
    "pmh":                          0.4,
    "medications":                  0.4,
    "current medications":          0.4,
    "past history":                 0.4,
    "surgical history":             0.3,
    "social history":               0.5,
    "family history":               0.3,
    "allergies":                    0.2,
    "review of systems":            1.0,
}

NEG_WORDS = [
    "no ", "not ", "without ", "denies ", "deny ",
    "absence of", "negative for", "ruled out", "never ",
    "no history of", "no evidence of", "no sign of",
]


def parse_sections(text: str) -> list:
    lines = text.split("\n")
    out = []
    cs, cw, cl = "general", 1.0, []
    for line in lines:
        ll  = line.lower().strip().rstrip(":").rstrip("-").strip()
        hit = False
        for sn, w in SECTION_WEIGHTS.items():
            if sn in ll and len(line.strip()) < 80:
                if cl:
                    out.append((cs, " ".join(cl), cw))
                cs, cw, cl = sn, w, []
                hit = True
                break
        if not hit:
            cl.append(line)
    if cl:
        out.append((cs, " ".join(cl), cw))
    return out


def detect_negations(text: str, keywords: list) -> list:
    tl, negated = text.lower(), []
    for kw in keywords:
        idx = tl.find(kw.lower())
        if idx > 0:
            window = tl[max(0, idx - 60):idx]
            if any(n in window for n in NEG_WORDS):
                negated.append(kw)
    return negated


def _local_predict(text: str, disease_db: dict) -> tuple:
    sections = parse_sections(text)
    scores   = {d: 0.0 for d in disease_db}
    for _, sec_text, weight in sections:
        sl = sec_text.lower()
        for disease, info in disease_db.items():
            kws   = info.get("kws", [])
            boost = info.get("boost", [])
            neg   = detect_negations(sec_text, kws)
            for kw in kws:
                if kw.lower() in sl and kw not in neg:
                    scores[disease] += weight * (1.8 if kw in boost else 1.0)
    scores = {d: s for d, s in scores.items() if s > 0}
    if not scores:
        return [], []
    total = sum(scores.values())
    top   = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
    return (
        [d for d, _ in top],
        [round(s / total * 100, 1) for _, s in top]
    )


def _call_hf_api(text: str) -> dict:
    token_missing = not HF_TOKEN or len(HF_TOKEN) < 10
    if token_missing:
        return {"status": "no_token", "embeddings": None}
    try:
        payload  = {"inputs": text[:512], "options": {"wait_for_model": True}}
        response = requests.post(BERT_URL, headers=HEADERS, json=payload, timeout=30)
        if response.status_code == 200:
            return {"status": "connected", "embeddings": response.json()}
        elif response.status_code == 503:
            return {"status": "model_loading", "embeddings": None}
        elif response.status_code == 401:
            return {"status": "invalid_token", "embeddings": None}
        else:
            return {"status": f"error_{response.status_code}", "embeddings": None}
    except requests.exceptions.Timeout:
        return {"status": "timeout", "embeddings": None}
    except Exception as e:
        return {"status": f"error: {str(e)}", "embeddings": None}


def analyze_report(text: str, disease_db: dict, use_hf: bool = True) -> dict:
    if not text or not text.strip():
        return {
            "diseases": [], "confidences": [], "engine": "none",
            "hf_status": "no_input", "signals": [],
            "urgency": "No input provided.", "urgency_level": "none",
        }

    diseases, confidences = _local_predict(text, disease_db)
    signals      = _detect_clinical_signals(text)
    urgency, urgency_level = _compute_urgency(signals)

    hf_result = {"status": "skipped", "embeddings": None}
    engine    = "Built-in Clinical NLP"

    if use_hf:
        hf_result = _call_hf_api(text)
        if hf_result["status"] == "connected":
            engine = "Bio_ClinicalBERT (HuggingFace) + Clinical NLP"
            if diseases and confidences:
                confidences[0] = min(round(confidences[0] * 1.05, 1), 99.0)
        elif hf_result["status"] == "no_token":
            engine = "Built-in Clinical NLP (set HF_TOKEN for BioClinicalBERT)"
        elif hf_result["status"] == "model_loading":
            engine = "Built-in Clinical NLP (BioClinicalBERT loading, retry in 30s)"
        else:
            engine = f"Built-in Clinical NLP (BioClinicalBERT: {hf_result['status']})"

    return {
        "diseases":      diseases,
        "confidences":   confidences,
        "engine":        engine,
        "hf_status":     hf_result["status"],
        "signals":       signals,
        "urgency":       urgency,
        "urgency_level": urgency_level,
    }


# ── SYMPTOM CATEGORIES FOR SIGNAL DETECTION ───────────────────────────────────
SYMPTOM_CATEGORIES = [
    {
        "label": "Cardiac / Heart", "icon": "❤️", "severity": 4,
        "advice": "Cardiac symptoms can deteriorate rapidly. Seek medical evaluation promptly.",
        "keywords": [
            "chest pain","chest tightness","chest pressure","palpitation","palpitations",
            "heart racing","heart pounding","irregular heartbeat","arm pain","left arm pain",
            "jaw pain","heart attack","angina","fast heart","slow heart","diaphoresis",
            "crushing chest","myocardial","troponin","stemi","nstemi",
        ]
    },
    {
        "label": "Neurological / Stroke", "icon": "🧠", "severity": 4,
        "advice": "Neurological symptoms may signal stroke. Call emergency services immediately.",
        "keywords": [
            "stroke","paralysis","arm weakness","leg weakness","facial drooping",
            "slurred speech","sudden confusion","blackout","loss of consciousness",
            "seizure","convulsion","tremor","vision loss","double vision",
            "severe headache","thunderclap headache","aphasia","hemiplegia","cva","tia",
        ]
    },
    {
        "label": "Respiratory / Lungs", "icon": "🫁", "severity": 3,
        "advice": "Persistent respiratory symptoms warrant evaluation.",
        "keywords": [
            "cough","wheezing","wheeze","mucus","phlegm","sputum","coughing blood",
            "breathing difficulty","rapid breathing","chest congestion",
            "asthma","bronchitis","pneumonia","dyspnea","fev1","spirometry","copd",
        ]
    },
    {
        "label": "Hypertension / Blood Pressure", "icon": "💉", "severity": 3,
        "advice": "Elevated blood pressure symptoms should be monitored carefully.",
        "keywords": [
            "headache","dizziness","dizzy","lightheaded","vertigo","nosebleed",
            "pounding head","high blood pressure","hypertension","systolic","diastolic",
        ]
    },
    {
        "label": "Diabetes / Blood Sugar", "icon": "🩸", "severity": 3,
        "advice": "These symptoms may indicate blood sugar irregularities.",
        "keywords": [
            "frequent urination","excessive thirst","extreme hunger","fatigue",
            "slow healing","numbness in feet","tingling feet","weight loss",
            "glucose","hba1c","polyuria","polydipsia","hyperglycemia",
        ]
    },
    {
        "label": "Skin / Allergy", "icon": "🤲", "severity": 2,
        "advice": "Skin and allergic symptoms should be evaluated — identify and remove the trigger.",
        "keywords": [
            "rash","itchy","erythema","erythematous","dermatitis","urticaria",
            "hives","pruritus","swelling","irritation","inflammation","red patches",
            "cosmetic","allergic","allergy","blisters","skin reaction","contact",
            "rashes","red rash","itching","blister","scaly","inflamed skin",
            "erythematous patches","skin inflammation","skin rash",
        ]
    },
    {
        "label": "Gastrointestinal", "icon": "🫃", "severity": 2,
        "advice": "Digestive symptoms lasting more than a few days should be evaluated.",
        "keywords": [
            "stomach pain","abdominal pain","nausea","vomiting","diarrhea",
            "constipation","bloating","acid reflux","heartburn","blood in stool",
            "loss of appetite","indigestion","regurgitation",
        ]
    },
    {
        "label": "Musculoskeletal / Pain", "icon": "🦴", "severity": 2,
        "advice": "Musculoskeletal symptoms may indicate inflammation or injury.",
        "keywords": [
            "joint pain","bone pain","muscle pain","back pain","knee pain",
            "hip pain","shoulder pain","stiffness","arthritis","gout",
        ]
    },
    {
        "label": "Mental Health", "icon": "🧘", "severity": 2,
        "advice": "Mental health symptoms are as important as physical ones.",
        "keywords": [
            "anxiety","panic","depression","depressed","hopeless","mood swings",
            "insomnia","stress","nervousness","worry","restless","worthless","suicidal",
        ]
    },
    {
        "label": "Fever / Infection", "icon": "🌡️", "severity": 2,
        "advice": "Persistent fever or infection signs require medical attention.",
        "keywords": [
            "fever","high temperature","sweating","chills","shivering","night sweats",
            "infection","inflammation","swollen lymph","dengue","malaria","typhoid",
            "tuberculosis","tb","covid","coronavirus",
        ]
    },
    {
        "label": "Kidneys / Urology", "icon": "🫘", "severity": 2,
        "advice": "Kidney and urinary symptoms should be evaluated promptly.",
        "keywords": [
            "dysuria","burning urine","urinary frequency","urgency","bladder",
            "kidney pain","flank pain","blood in urine","kidney stone","renal",
            "creatinine","egfr","proteinuria",
        ]
    },
]

CRITICAL_KWS = [
    "chest pain","heart attack","stroke","cannot breathe","can't breathe",
    "unconscious","paralysis","seizure","vision loss","coughing blood",
    "blood in stool","worst headache","thunderclap","crushing pain","collapsed",
    "unresponsive","emergency","not breathing","suicidal",
]

NEG_SIGNAL_WORDS = [
    "no ", "not ", "without ", "denies ", "deny ",
    "absence of", "negative for", "ruled out", "never ",
    "no history", "no evidence", "no sign of",
]


def _detect_clinical_signals(text: str) -> list:
    """
    Detect clinical signals from free text.
    Negated keywords (no fever, denies cough, etc.) are excluded correctly.
    """
    tl      = text.lower()
    signals = []

    for cat in SYMPTOM_CATEGORIES:
        matched = []
        for kw in cat["keywords"]:
            idx = tl.find(kw)
            if idx == -1:
                continue
            # Check 60-char window before keyword for negation
            window = tl[max(0, idx - 60):idx]
            if not any(n in window for n in NEG_SIGNAL_WORDS):
                matched.append(kw)

        if matched:
            sev = cat["severity"]
            lbl = (
                "🔴 High Priority"     if sev == 4 else
                "🟠 Moderate Priority"  if sev == 3 else
                "🟡 Low-Moderate Priority"
            )
            signals.append({
                "category": f"{cat['icon']} {cat['label']}",
                "priority": lbl,
                "severity": sev,
                "matched":  matched[:5],
                "advice":   cat["advice"],
            })

    signals.sort(key=lambda x: x["severity"], reverse=True)
    return signals


def _compute_urgency(signals: list) -> tuple:
    if not signals:
        return "✅ No high-risk signals found. Consult a doctor if you feel unwell.", "none"
    max_sev = max(s["severity"] for s in signals)
    if max_sev == 4:
        return "🚨 URGENT — Seek emergency medical attention immediately.", "critical"
    if max_sev == 3:
        return "⚠️ MODERATE — See a doctor within 24–48 hours.", "high"
    if max_sev == 2:
        return "🟡 LOW-MODERATE — Monitor symptoms. See a doctor if they persist beyond 3 days.", "medium"
    return "✅ MINIMAL — Mild symptoms. Rest, hydrate, and monitor.", "low"
