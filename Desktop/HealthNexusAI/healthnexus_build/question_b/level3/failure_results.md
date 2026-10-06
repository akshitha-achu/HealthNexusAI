# Question B — Actual Failure Evidence

Run:
```powershell
python scripts\failure_demo.py
```

Paste the actual terminal output below. Then add my own before/after explanation.

## Failure 1 — Missing model
Before: [actual output]
Root cause: [my explanation]
Fix: restore/retrain `models/logistic_regression.joblib`
After: [actual successful response]

## Failure 2 — Invalid input
Before: [actual output]
Root cause: [my explanation]
Fix: Pydantic validation with age range 1–120
After: [actual validation response]
