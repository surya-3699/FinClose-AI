from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os

from app.demo_data import demo_data
from app.reconciliation import reconcile, metrics


app = FastAPI(
    title="FinClose AI",
    version="1.0.0",
    description="Agentic financial reconciliation and exception controller"
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add deployed frontend URL from environment variable
frontend_url = os.getenv("FRONTEND_URL")

if frontend_url:
    allowed_origins.append(frontend_url)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# APPLICATION STATE
# --------------------------------------------------

state = {
    "results": [],
    "metrics": {},
    "settlements": [],
    "ledger": []
}


# --------------------------------------------------
# RECONCILIATION RUNNER
# --------------------------------------------------

def run(settlements, ledger):
    state["settlements"] = settlements
    state["ledger"] = ledger

    state["results"] = reconcile(settlements, ledger)
    state["metrics"] = metrics(state["results"])

    return {
        "metrics": state["metrics"],
        "results": state["results"]
    }


# --------------------------------------------------
# BASIC ENDPOINTS
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "name": "FinClose AI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# DEMO DATA
# --------------------------------------------------

@app.post("/api/demo/load")
def load_demo():
    settlements, ledger = demo_data()
    return run(settlements, ledger)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.get("/api/dashboard")
def dashboard():
    return {
        "metrics": state["metrics"],
        "results": state["results"],
        "settlements_count": len(state["settlements"]),
        "ledger_count": len(state["ledger"])
    }


# --------------------------------------------------
# CSV RECONCILIATION
# --------------------------------------------------

@app.post("/api/reconcile")
def reconcile_csv(
    settlements_file: UploadFile = File(...),
    ledger_file: UploadFile = File(...)
):
    try:
        s_df = pd.read_csv(
            io.BytesIO(settlements_file.file.read())
        )

        l_df = pd.read_csv(
            io.BytesIO(ledger_file.file.read())
        )

        required = {
            "id",
            "reference",
            "amount",
            "date"
        }

        if not required.issubset(set(s_df.columns)):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Settlement CSV requires "
                    "id, reference, amount and date columns."
                )
            )

        if not required.issubset(set(l_df.columns)):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Ledger CSV requires "
                    "id, reference, amount and date columns."
                )
            )

        settlements = (
            s_df.fillna("")
            .to_dict(orient="records")
        )

        ledger = (
            l_df.fillna("")
            .to_dict(orient="records")
        )

        for item in settlements:
            item["source"] = "settlement"

        for item in ledger:
            item["source"] = "ledger"

        return run(settlements, ledger)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to process CSV files: {exc}"
        )


# --------------------------------------------------
# EXCEPTIONS
# --------------------------------------------------

@app.get("/api/exceptions")
def exceptions():
    return [
        result
        for result in state["results"]
        if result["status"] != "reconciled"
    ]


# --------------------------------------------------
# INVESTIGATION
# --------------------------------------------------

@app.get("/api/investigate/{settlement_id}")
def investigate(settlement_id: str):

    item = next(
        (
            result
            for result in state["results"]
            if result["settlement_id"] == settlement_id
        ),
        None
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    action = (
        "Approve automatically"
        if item["status"] == "reconciled"
        else "Request human review"
        if item["status"] == "needs_review"
        else "Investigate source data and supporting documents"
    )

    return {
        "transaction": item,
        "controller_recommendation": action,
        "audit_note": (
            "This explanation is generated from reconciliation "
            "evidence. Low-confidence cases are not automatically approved."
        )
    }