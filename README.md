# NyayaAI – AI-Powered Legal Case Analysis & Outcome Prediction System

NyayaAI is a production-grade AI-powered legal research and case analysis platform built for the Indian legal context. The application uses Natural Language Processing (NLP) parameter extraction, semantic vector search, Retrieval-Augmented Generation (RAG), and custom explainable classification models to evaluate case facts, recommend statutory sections, locate similar historical precedents, and predict historical outcome trends.

> [!IMPORTANT]
> **LEGAL SAFETY DISCLAIMER:** NyayaAI is an educational research assistance tool. It does NOT act as an advocate or judge, does NOT replace professional legal counsel, and does NOT guarantee case results in a court of law. All predictions are informational simulations based on historic precedent correlations.

---

## 🚀 Quick Start (Single Command)

If you are on Windows, simply double-click the **`run.bat`** file in the root directory. This will start:
1. **FastAPI Backend Server** on `http://127.0.0.1:8000` (auto-creates and seeds the SQLite database)
2. **Vite React Frontend Server** on `http://localhost:5173`

---

## 🔑 Demo Login Accounts

Use these pre-seeded accounts to explore role-specific features:

| Role | Username | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Client** | `client` | `client123` | Submit cases, view analysis dashboard, download PDF dockets. |
| **Lawyer** | `lawyer` | `lawyer123` | Explore judgments database, add research notes, bookmark cases. |
| **Admin** | `admin` | `admin123` | Inspect model F1/AUC metrics, retrain classifier, ingest records. |

---

## 🛠️ System Architecture & Technology Stack

```
                     +----------------------------------------+
                     |         Vite + React Frontend          |
                     |  (Tailwind CSS, TypeScript, Recharts)  |
                     +-------------------+--------------------+
                                         |
                                         | REST APIs (JWT)
                                         v
                     +-------------------+--------------------+
                     |         FastAPI Backend Core           |
                     |  (Uvicorn, SQLAlchemy ORM, SQLite DB)  |
                     +-------------------+--------------------+
                                         |
            +----------------------------+----------------------------+
            |                            |                            |
            v                            v                            v
+-----------+-----------+    +-----------+-----------+    +-----------+-----------+
|    NLP extraction     |    |   Classifier Engine   |    |    Vector Search      |
|  (Regex & Heuristics) |    |  (TF-IDF + LogReg)    |    |  (Cosine Similarity)  |
+-----------------------+    +-----------------------+    +-----------------------+
```

### Stack Components:
- **Frontend:** React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons, Recharts.
- **Backend:** Python 3.12, FastAPI, Uvicorn, SQLAlchemy, Pydantic, PyJWT, bcrypt.
- **AI/ML:** scikit-learn (TF-IDF Vectorizer, Logistic Regression), numpy, pandas, sentence-transformers (pluggable).
- **Reports:** fpdf2 (native PDF creation).

---

## 📁 Project Directory Structure

```
nyaya-ai/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entry point & Seeding
│   │   ├── config.py              # Settings config
│   │   ├── database.py            # SQLite connections
│   │   ├── models/                # SQLAlchemy models (auth, legal, chat)
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── routers/               # APIRoutes (auth, cases, legal, chat, admin)
│   │   ├── services/              # AI engines (nlp, classifier, similarity, outcome, RAG, reports)
│   │   └── utils/                 # Security, JWT
│   └── requirements.txt           # Pip dependencies
├── frontend/
│   ├── src/
│   │   ├── components/            # Navbars, layout
│   │   ├── pages/                 # Full screens (Landing, Dashboard, Analysis, Chat, Admin)
│   │   ├── services/              # api.ts fetch client
│   │   ├── App.tsx                # Client router state
│   │   └── main.tsx               # Bootstrap mounts
│   └── tailwind.config.js         # Styling configs
├── data/
│   └── demo/
│       ├── legal_cases.csv        # 125 pre-made judgments
│       └── legal_sections.csv     # 110 statutory sections
├── run.bat                        # Launcher batch file
└── README.md                      # This documentation file
```

---

## 🎯 Verification and Manual Testing Walkthrough

1. **Submission:** Log in as `client`, click **Submit Legal Problem**, write details of a lease dispute (e.g., "My landlord Ramesh is refusing to return my security deposit of Rs. 50,000 for my apartment in Bangalore...").
2. **Processing:** The system executes the extraction timeline, maps the category to *Property Law / Landlord-Tenant disputes*, and suggests *Transfer of Property Act* sections.
3. **Outcome:** View the outcome dial (e.g., 70% Favorable probability) and read the explanation (e.g., written contract exists).
4. **Precedents:** Open the **Side-by-Side Comparison** modal to evaluate your facts against a historic precedent.
5. **Simulation:** Use the **Factual Simulator ("What If?")** to untick "Written Agreement Exists" and click **Simulate**. See the Favorable dial drop from ~70% to ~45% dynamically due to lack of civil lease contract deeds.
6. **Chatbot:** Navigate to the **Research Chat** tab, ask: *"What is the penalty for cheque bounce under Section 138?"* and read the citation-verified summary pointing to the Negotiable Instruments Act.
7. **Report:** Click **Generate PDF Report** from the case page to export a structured, styled case evaluation document.
