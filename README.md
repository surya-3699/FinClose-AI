# FinClose AI — Agentic Financial Reconciliation & Exception Controller

> Razorpay AI Builder Internship 2026 — Track 4: AI Finance Controller

FinClose AI reconciles payment settlement records against an internal ledger using a layered controller:
1. deterministic exact matching,
2. fuzzy candidate matching,
3. conservative confidence thresholds,
4. explainable exception handling,
5. optional AI investigation for ambiguous records.

The project is intentionally designed so the core financial workflow works **without an LLM API key**. AI integration is an optional enhancement, not a dependency for correctness.

## What it solves

Finance teams often receive payment settlements and internal ledger exports with:
- inconsistent transaction references,
- date shifts,
- duplicate records,
- fees and net settlements,
- partial information,
- unmatched transactions.

FinClose AI ingests two CSV files, normalizes records, matches them safely, calculates reconciliation metrics, and creates an exception queue for human review.

## Architecture

```text
CSV Uploads
   |
   v
FastAPI Ingestion
   |
   v
Normalization
   |
   +--> Exact Match Engine
   |
   +--> Fuzzy Match Engine
   |
   v
Confidence Controller
   |
   +--> Auto Reconciled
   |
   +--> Needs Review
   |
   +--> Exception Queue
   |
   v
Dashboard + Audit Trail
```

## Tech stack

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite by default (easy demo), PostgreSQL-ready
- Pandas
- RapidFuzz
- Pydantic
- Pytest

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- Recharts

## Quick start

### Option A — Docker

```bash
docker compose up --build
```

Open:
- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs

### Option B — Local

Backend:

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Demo flow

1. Open the dashboard.
2. Click **Load Demo Dataset**.
3. Review total settlement and ledger records.
4. Inspect auto-matched transactions.
5. Open the exception queue.
6. Select an ambiguous transaction.
7. Show the evidence and recommended action.
8. Explain that low-confidence cases are intentionally not auto-approved.

## Safety principles

- No fabricated financial decisions.
- Low-confidence matches remain exceptions.
- Every result includes a reason and evidence.
- AI is optional and cannot silently override deterministic controls.
- Demo data is synthetic.

## Testing

```bash
cd backend
pytest -q
```

## Repository checklist before submission

- [ ] Public GitHub repository
- [ ] README updated with screenshots
- [ ] Demo video link added
- [ ] Tests passing
- [ ] `.env.example` included
- [ ] No secrets committed
- [ ] Deployment link verified
- [ ] GitHub repository URL copied into form

## Suggested submission title

**FinClose AI — Agentic Financial Reconciliation & Exception Controller**

## Suggested project objective

FinClose AI automates the finance reconciliation loop by ingesting payment settlements and internal ledger records, normalizing inconsistent transaction data, matching records using deterministic and similarity-based methods, escalating ambiguous cases for explainable AI-assisted investigation, and producing an auditable reconciliation report with confidence scores and a complete exception queue.

