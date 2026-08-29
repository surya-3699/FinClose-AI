# Razorpay Submission Guide — FinClose AI

## Track
Track 4: AI Finance Controller

## Project Name / Title
FinClose AI — Agentic Financial Reconciliation & Exception Controller

## Project Objectives
FinClose AI automates the finance reconciliation loop by ingesting payment settlements and internal ledger records, normalizing inconsistent transaction data, matching records using deterministic and similarity-based methods, escalating ambiguous cases for explainable AI-assisted investigation, and producing an auditable reconciliation report with confidence scores and a complete exception queue.

The objective is not to replace financial judgment with a chatbot. The system acts as a finance controller: automate high-confidence work, expose uncertainty, and preserve a clear audit trail for human decisions.

## GitHub Repository URL
After creating the repository and pushing this project, paste:

https://github.com/YOUR_USERNAME/finclose-ai

Do not submit this placeholder.

## 5-minute pitch structure

### 0:00–0:30 — Problem
“Finance reconciliation is still full of repetitive manual comparison. Payment settlements and internal ledgers frequently disagree because references are inconsistent, dates shift, duplicates appear, and some transactions are missing.”

### 0:30–1:00 — Solution
“FinClose AI is an AI Finance Controller. It does not blindly let an LLM decide financial records. It uses a layered controller: deterministic matching first, similarity matching second, and AI-assisted investigation only for ambiguity.”

### 1:00–2:45 — Demo
1. Load demo dataset.
2. Show dashboard metrics.
3. Open an exact match.
4. Open a fuzzy match.
5. Open a needs-review case.
6. Open an unmatched exception.
7. Explain evidence and confidence.

### 2:45–3:45 — Technical depth
Explain normalization, exact matching, fuzzy similarity, confidence thresholds, exception queue, evidence and optional LLM investigation.

### 3:45–4:30 — Why this is safer
“Low-confidence transactions are not auto-approved. The system can abstain. Every recommendation has a reason and evidence.”

### 4:30–5:00 — Impact
“FinClose AI reduces repetitive reconciliation work while making unresolved financial risk visible instead of hiding it behind a chatbot.”

## Build Challenges & Technical Obstacles
The main challenge was balancing automation with financial reliability. Real transaction data can contain inconsistent references, date shifts, duplicate records, and ambiguous candidates. A single AI prompt would be unsafe because a plausible explanation is not proof of a financial match.

I solved this by designing a layered reconciliation pipeline: deterministic matching handles exact evidence, fuzzy matching handles formatting differences, conservative confidence thresholds prevent unsafe auto-approval, and unresolved cases are explicitly routed to review. I also designed the AI layer as an investigator rather than a source of truth, requiring structured evidence-linked recommendations and allowing abstention.

## Before clicking Submit
- Run backend tests.
- Run frontend build.
- Record the demo.
- Push final code to GitHub.
- Verify the repository is public.
- Open the repo in an incognito browser.
- Check README rendering.
- Verify video link permissions.
- Fill the form.
- Read every field once.
- Tick final confirmation only when everything is final.
