# 🏥 MedReport AI v7.0

> Clinical NLP report analyser — BioClinicalBERT + 51 diseases + plain-English output

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

App opens at **http://localhost:8501**

---

## Project Structure

```
MedReport/
│
├── app.py                        ← Entry point (run this)
├── requirements.txt
│
├── backend/                      ← All logic, NO UI here
│   ├── modules/
│   │   ├── diseases.py           ← 51-disease knowledge base (10 categories)
│   │   ├── clinicalbert.py       ← BioClinicalBERT + built-in NLP engine
│   │   ├── predictor.py          ← Prediction orchestrator
│   │   ├── logger.py             ← Audit logging (audit_log.json)
│   │   └── dataloader.py         ← CSV / PDF / TXT loading + sample notes
│   ├── data/
│   │   └── clinical_notes.csv    ← Sample patient dataset
│   └── results/
│       └── audit_log.json        ← Auto-generated prediction history
│
└── frontend/                     ← All UI, NO business logic here
    ├── components/
    │   ├── styles.py             ← ALL CSS in one place
    │   ├── sidebar.py            ← Sidebar navigation + settings
    │   ├── charts.py             ← Matplotlib chart builders
    │   └── cards.py              ← Reusable HTML card components
    └── pages/
        ├── check_report.py       ← Page 1: Upload + predict + results
        ├── disease_guide.py      ← Page 2: Colorful disease card guide
        ├── browse_records.py     ← Page 3: Dataset explorer
        ├── history.py            ← Page 4: Audit log viewer
        └── how_it_works.py       ← Page 5: Pipeline explainer
```

---

## BioClinicalBERT Setup (optional)

Get a free token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

```bash
# Option 1 — paste in sidebar
# Option 2 — environment variable
set HF_TOKEN=hf_your_token_here       # Windows
export HF_TOKEN=hf_your_token_here    # Mac/Linux
```

Without a token the built-in clinical NLP engine runs automatically.

---

## What Each Module Does

| Module | Responsibility |
|--------|---------------|
| `diseases.py` | 51-disease knowledge base with keywords, medicines, specialists |
| `clinicalbert.py` | HuggingFace API call + section parser + negation detection |
| `predictor.py` | Orchestrates prediction, enriches with disease info |
| `logger.py` | Saves every prediction to `audit_log.json` |
| `dataloader.py` | Loads CSV dataset, extracts PDF text, provides sample notes |
| `styles.py` | All CSS — one file to update the entire UI look |
| `sidebar.py` | Navigation, token input, settings |
| `charts.py` | Confidence bar chart + dataset distribution chart |
| `cards.py` | Hero card, result tabs, organ tiles, disease feature cards |

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**.  
Not a substitute for professional medical advice. Always consult a qualified doctor.
