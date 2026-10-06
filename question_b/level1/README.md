# Question B — Level 1: Build

FastAPI serves a trained Logistic Regression model through `POST /predict` and the static frontend consumes that endpoint. The app stores prediction results in SQLite.

Run:
```powershell
python scripts\prepare_data.py
python scripts\train_model.py
python -m uvicorn app.main:app --reload
```
