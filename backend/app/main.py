from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from app.demo_data import demo_data
from app.reconciliation import reconcile, metrics

app = FastAPI(title="FinClose AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

state = {"results": [], "metrics": {}, "settlements": [], "ledger": []}

def run(settlements, ledger):
    state["settlements"] = settlements
    state["ledger"] = ledger
    state["results"] = reconcile(settlements, ledger)
    state["metrics"] = metrics(state["results"])
    return {"metrics": state["metrics"], "results": state["results"]}

@app.get("/")
def root():
    return {"name": "FinClose AI", "status": "running"}

@app.post("/api/demo/load")
def load_demo():
    settlements, ledger = demo_data()
    return run(settlements, ledger)

@app.get("/api/dashboard")
def dashboard():
    return {
        "metrics": state["metrics"],
        "results": state["results"],
        "settlements_count": len(state["settlements"]),
        "ledger_count": len(state["ledger"])
    }

@app.post("/api/reconcile")
def reconcile_csv(
    settlements_file: UploadFile = File(...),
    ledger_file: UploadFile = File(...)
):
    try:
        s_df = pd.read_csv(io.BytesIO(settlements_file.file.read()))
        l_df = pd.read_csv(io.BytesIO(ledger_file.file.read()))
        required = {"id", "reference", "amount", "date"}
        if not required.issubset(set(s_df.columns)) or not required.issubset(set(l_df.columns)):
            raise HTTPException(status_code=400, detail="CSV files require id, reference, amount and date columns.")
        settlements = s_df.fillna("").to_dict(orient="records")
        ledger = l_df.fillna("").to_dict(orient="records")
        for x in settlements: x["source"] = "settlement"
        for x in ledger: x["source"] = "ledger"
        return run(settlements, ledger)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to process CSV files: {exc}")

@app.get("/api/exceptions")
def exceptions():
    return [r for r in state["results"] if r["status"] != "reconciled"]

@app.get("/api/investigate/{settlement_id}")
def investigate(settlement_id: str):
    item = next((r for r in state["results"] if r["settlement_id"] == settlement_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Transaction not found")
    action = (
        "Approve automatically" if item["status"] == "reconciled"
        else "Request human review" if item["status"] == "needs_review"
        else "Investigate source data and supporting documents"
    )
    return {
        "transaction": item,
        "controller_recommendation": action,
        "audit_note": "This explanation is generated from reconciliation evidence. Low-confidence cases are not automatically approved."
    }
