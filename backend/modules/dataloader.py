"""
backend/modules/dataloader.py
===============================
Data loading utilities — CSV dataset, PDF extraction, TXT loading.
"""

import os
import pandas as pd
import pdfplumber

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CSV_PATH = os.path.join(DATA_DIR, "clinical_notes.csv")


def load_dataset() -> pd.DataFrame:
    """Load clinical_notes.csv from the data directory."""
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    # Fallback — check current working directory
    if os.path.exists("clinical_notes.csv"):
        return pd.read_csv("clinical_notes.csv")
    return pd.DataFrame()


def extract_pdf(file_obj) -> str:
    """Extract text from an uploaded PDF file object."""
    text = ""
    try:
        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        text = f"[PDF extraction error: {str(e)}]"
    return text


def load_txt(file_obj) -> str:
    """Decode an uploaded TXT file object to string."""
    try:
        return file_obj.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def get_sample_notes() -> dict:
    """
    Return built-in example clinical notes for 10 conditions.
    Used in the frontend when user selects 'Use an example'.
    """
    return {
        "🫁 COPD": (
            "Chief Complaint\nChronic productive cough, progressive shortness of breath "
            "and wheeze for 6 months.\n\nHistory of Present Illness\n62-year-old male with "
            "40-pack-year smoking history. Worsening dyspnea on exertion and chronic "
            "productive cough with yellowish sputum. Audible wheeze in the mornings. "
            "Denies fever or chest pain.\n\nPast Medical History\nType 2 Diabetes on "
            "Metformin. Hypertension on Amlodipine.\n\nInvestigations\nSpirometry: "
            "FEV1/FVC 0.54. FEV1 51% predicted. Barrel chest. Hyperinflation on CXR. "
            "SpO2 91%.\n\nAssessment\nModerate-to-severe COPD, GOLD Stage III."
        ),
        "❤️ Heart Attack": (
            "Chief Complaint\nSudden severe crushing chest pain for 45 minutes.\n\n"
            "History of Present Illness\n58-year-old male with sudden onset severe "
            "crushing chest pain radiating to left arm and jaw. Associated with "
            "diaphoresis, nausea and breathlessness.\n\nInvestigations\nECG: ST "
            "elevation leads II,III,aVF. Troponin 2.4 ng/mL elevated.\n\nAssessment\n"
            "Acute inferior STEMI. Urgent PCI required."
        ),
        "🩸 Type 2 Diabetes": (
            "Chief Complaint\nPolyuria and excessive thirst for 3 months.\n\n"
            "History of Present Illness\n45-year-old female with polyuria, polydipsia "
            "and unexplained weight loss. Fasting glucose 11.2 mmol/L. HbA1c 8.9%. "
            "BMI 31.\n\nAssessment\nType 2 Diabetes Mellitus. Commence Metformin 500mg."
        ),
        "🧠 Migraine": (
            "Chief Complaint\nRecurrent severe throbbing headache on one side.\n\n"
            "History of Present Illness\n28-year-old female with migraine — unilateral "
            "throbbing headache with nausea, photophobia and visual aura (zigzag lines). "
            "Attacks last 4-72 hours. Triggered by stress."
        ),
        "🌡️ Pneumonia": (
            "Chief Complaint\nHigh fever and productive cough for 4 days.\n\n"
            "History of Present Illness\n67-year-old male. Fever 39.2C, productive "
            "cough with purulent sputum, pleuritic chest pain. Right lower lobe "
            "consolidation on CXR. WBC elevated. SpO2 94%.\n\nAssessment\n"
            "Community-acquired pneumonia right lower lobe."
        ),
        "🦠 Dengue Fever": (
            "Chief Complaint\nHigh fever and severe body pain for 3 days.\n\n"
            "History of Present Illness\nSudden onset fever 40C, severe retroorbital "
            "headache, myalgia and arthralgia. NS1 antigen positive. Platelet count "
            "85,000. Rash on trunk. Dengue IgM positive."
        ),
        "🧘 Anxiety": (
            "Chief Complaint\nExcessive worry and panic attacks for 6 months.\n\n"
            "History of Present Illness\nPersistent anxiety, worry and panic attacks. "
            "Palpitations, restlessness, difficulty sleeping and nervousness. "
            "GAD-7 score 16 severe."
        ),
        "💧 UTI": (
            "Chief Complaint\nBurning urination and urinary frequency for 3 days.\n\n"
            "History of Present Illness\n25-year-old female. Dysuria, urinary frequency "
            "and urgency. Burning sensation on urination. Cloudy urine. Urine dipstick "
            "positive for nitrites and leukocytes. No fever."
        ),
        "🧠 Stroke": (
            "Chief Complaint\nSudden onset weakness and slurred speech.\n\n"
            "History of Present Illness\n72-year-old male with sudden onset left "
            "hemiplegia, facial drooping and aphasia. CT brain: right MCA territory "
            "infarction. History of hypertension and atrial fibrillation. CVA confirmed."
        ),
        "🤲 Skin Allergy (Contact Dermatitis)": (
            "Chief Complaint\nItchy red rashes on both arms and neck for 3 days.\n\n"
            "History of Present Illness\nSymptoms started after using a new cosmetic "
            "product. Mild swelling and irritation present. No fever or breathing "
            "difficulty.\n\nPhysical Examination\nErythematous patches with mild "
            "inflammation on both arms and neck. Pruritus noted. Dermatitis appearance "
            "consistent with contact reaction."
        ),
    }
