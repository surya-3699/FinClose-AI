from pydantic import BaseModel
from typing import Optional, List

class Transaction(BaseModel):
    id: str
    reference: str
    amount: float
    date: str
    customer: str = ""
    status: str = "unknown"
    source: str

class MatchResult(BaseModel):
    settlement_id: str
    ledger_id: Optional[str] = None
    status: str
    confidence: float
    method: str
    reason: str
    evidence: List[str] = []
