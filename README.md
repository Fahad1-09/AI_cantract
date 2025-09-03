# 📑 AI Contract Drafter

AI-powered application for **contract drafting, compliance checking, and summarization**.  
It combines a **FastAPI backend** and a **Streamlit frontend** to provide an end-to-end workflow:
1. Upload project details or base contracts.
2. Generate a first draft using AI + Pinecone retrieval.
3. Run compliance and risk analysis.
4. Generate a plain-English summary.
5. Export the final contract.

---

## 🚀 Features
- **Project Input Form**: Enter company, project scope, tools, duration, and deliverables.  
- **AI Drafting**: Automatically drafts contracts based on input + template chunks.  
- **Compliance Check**: Flags missing clauses and risks (GDPR, IP, liability, etc.).  
- **Summary Generation**: Produces a concise plain-English overview.  
- **Export Options**: Download drafted contracts in text format.  

---

## 🛠️ Tech Stack
- **Backend**: FastAPI  
- **Frontend**: Streamlit  
- **Vector DB**: Pinecone  
- **AI Model**: Google Gemini (Generative API)  
- **PDF Parsing**: PyPDF2 / custom text splitter  

---

## 📂 Project Structure
```
contract-drafter/
│
├── Fastapi/                 # Backend
│   ├── app.py               # FastAPI entrypoint
│   ├── pinecone_utilis.py   # Pinecone embedding + storage
│   ├── services/            # Core business logic
│   │   ├── pdf_parsing.py
│   │   ├── drafting.py
│   │   ├── compliance.py
│   │   ├── summary.py
│   ├── schema/              # Pydantic models
│   │   ├── pydantic_models.py
│   ├── session_memory.py    # Session store
│   └── prompts/             # Prompt templates
│
├── Frontend/
│   ├── main.py              # Streamlit UI
│
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the repo
```bash
git clone https://github.com/Fahad1-09/AI_cantract.git
cd contract-drafter
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
Create a `.env` file with:
```ini
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=legal-docs
GOOGLE_API_KEY=your_gemini_key
```

### 5. Run backend (FastAPI)
```bash
uvicorn Fastapi.app:app --reload --port 9000
```
Backend runs at: [http://127.0.0.1:9000](http://127.0.0.1:9000)

### 6. Run frontend (Streamlit)
```bash
streamlit run Frontend/main.py
```

Frontend runs at: [http://localhost:8501](http://localhost:8501)

---

## 📌 API Endpoints

| Endpoint          | Method | Description |
|-------------------|--------|-------------|
| `/ingest-pdf/`    | POST   | Upload and embed a base PDF contract |
| `/input/`         | POST   | Submit project details |
| `/retrieve/`      | POST   | Retrieve template contract chunks |
| `/draft/`         | POST   | Generate AI-drafted contract |
| `/compliance/`    | POST   | Run compliance and risk analysis |
| `/summary/`       | POST   | Generate plain-English summary |

---

## 📸 UI Workflow
1. **Project Details Page** → Enter input fields  
2. **Draft Contract Page** → Generate AI draft  
3. **Compliance Check Page** → Get compliance insights  
4. **Summary & Export Page** → View summary & download draft  

---

## 📥 Example Project Input
```json
{
  "company_name": "TechNova Solutions",
  "project_name": "AI Resume Screening System",
  "project_scope": "Develop AI-powered resume parsing and ranking system with HRMS integration.",
  "tools": "Python, FastAPI, Pinecone, Streamlit",
  "duration": "120 days",
  "deliverables": "Resume parsing module, ranking engine, HRMS integration, dashboard, documentation"
}

