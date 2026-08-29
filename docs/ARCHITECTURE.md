# FinClose AI Architecture

```mermaid
flowchart LR
A[Settlement CSV] --> C[Normalizer]
B[Ledger CSV] --> C
C --> D[Exact Match Engine]
C --> E[Fuzzy Candidate Engine]
D --> F[Confidence Controller]
E --> F
F -->|High confidence| G[Reconciled]
F -->|Medium confidence| H[Human Review]
F -->|No safe candidate| I[Exception Queue]
H --> J[AI Investigator Optional]
J --> K[Evidence + Recommendation]
G --> L[Dashboard + Audit Trail]
H --> L
I --> L
```

## Design decision
The AI component is deliberately constrained. Financial correctness comes from transaction evidence and deterministic controls. AI is used to explain and investigate ambiguity, not to invent matches.
