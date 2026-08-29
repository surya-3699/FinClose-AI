from __future__ import annotations
import re
from datetime import datetime
from rapidfuzz.fuzz import ratio

def norm_ref(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).lower())

def parse_date(value: str):
    try:
        return datetime.fromisoformat(str(value)).date()
    except Exception:
        return None

def reconcile(settlements, ledger):
    used = set()
    results = []

    for s in settlements:
        best = None

        # Layer 1: exact reference + exact amount
        for l in ledger:
            if l["id"] in used:
                continue
            if norm_ref(s["reference"]) == norm_ref(l["reference"]) and abs(float(s["amount"]) - float(l["amount"])) < 0.01:
                best = {
                    "ledger_id": l["id"],
                    "status": "reconciled",
                    "confidence": 1.0,
                    "method": "exact",
                    "reason": "Reference and amount matched exactly.",
                    "evidence": [
                        f"Settlement reference: {s['reference']}",
                        f"Ledger reference: {l['reference']}",
                        f"Amount: {s['amount']}"
                    ]
                }
                break

        # Layer 2: amount + date proximity + fuzzy reference
        if best is None:
            candidates = []
            for l in ledger:
                if l["id"] in used:
                    continue
                amount_diff = abs(float(s["amount"]) - float(l["amount"]))
                ref_score = ratio(norm_ref(s["reference"]), norm_ref(l["reference"])) / 100
                sd, ld = parse_date(s["date"]), parse_date(l["date"])
                day_gap = abs((sd - ld).days) if sd and ld else 99
                date_score = max(0, 1 - day_gap / 7)

                if amount_diff < 0.01:
                    confidence = 0.70 * ref_score + 0.30 * date_score
                    candidates.append((confidence, l, ref_score, day_gap))

            if candidates:
                confidence, l, ref_score, day_gap = max(candidates, key=lambda x: x[0])
                if confidence >= 0.86:
                    best = {
                        "ledger_id": l["id"],
                        "status": "reconciled",
                        "confidence": round(confidence, 3),
                        "method": "fuzzy",
                        "reason": "Amount matched and transaction reference/date strongly aligned.",
                        "evidence": [
                            f"Reference similarity: {round(ref_score * 100, 1)}%",
                            f"Date gap: {day_gap} day(s)",
                            "Amount matched exactly"
                        ]
                    }
                elif confidence >= 0.60:
                    best = {
                        "ledger_id": l["id"],
                        "status": "needs_review",
                        "confidence": round(confidence, 3),
                        "method": "fuzzy_review",
                        "reason": "A plausible candidate exists, but confidence is below the safe auto-match threshold.",
                        "evidence": [
                            f"Reference similarity: {round(ref_score * 100, 1)}%",
                            f"Date gap: {day_gap} day(s)",
                            "Human review required"
                        ]
                    }

        if best is None:
            best = {
                "ledger_id": None,
                "status": "exception",
                "confidence": 0.0,
                "method": "unmatched",
                "reason": "No sufficiently reliable ledger candidate was found.",
                "evidence": ["No candidate passed reconciliation thresholds"]
            }
        else:
            if best["status"] == "reconciled" and best["ledger_id"]:
                used.add(best["ledger_id"])

        results.append({
            "settlement_id": s["id"],
            "settlement_reference": s["reference"],
            "settlement_amount": float(s["amount"]),
            **best
        })

    matched_ledger = {r["ledger_id"] for r in results if r.get("ledger_id") and r["status"] == "reconciled"}
    orphan_ledger = [
        {
            "settlement_id": None,
            "settlement_reference": None,
            "settlement_amount": None,
            "ledger_id": l["id"],
            "status": "exception",
            "confidence": 0.0,
            "method": "orphan_ledger",
            "reason": "Ledger transaction has no reconciled settlement.",
            "evidence": ["No settlement was safely matched"]
        }
        for l in ledger if l["id"] not in matched_ledger
    ]

    return results + orphan_ledger

def metrics(results):
    total = len(results)
    reconciled = sum(r["status"] == "reconciled" for r in results)
    review = sum(r["status"] == "needs_review" for r in results)
    exceptions = sum(r["status"] == "exception" for r in results)
    avg_conf = sum(r["confidence"] for r in results) / total if total else 0
    return {
        "total_items": total,
        "reconciled": reconciled,
        "needs_review": review,
        "exceptions": exceptions,
        "reconciliation_rate": round((reconciled / total * 100) if total else 0, 2),
        "average_confidence": round(avg_conf * 100, 2)
    }
