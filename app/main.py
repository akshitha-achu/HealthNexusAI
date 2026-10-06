from pathlib import Path
import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .config import MODEL_PATH, ROOT
from .database import init_db, save_prediction, stats, recent
from .schemas import PredictionRequest
from .rag import rank_chunks, library_rank_chunks, ask_health_ai

app = FastAPI(title='HealthNexus AI', version='1.0.0')
FRONTEND = ROOT / 'frontend'
app.mount('/static', StaticFiles(directory=FRONTEND), name='static')

FEATURES = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']

@app.on_event('startup')
def startup():
    init_db()

@app.get('/')
def home():
    return FileResponse(FRONTEND / 'index.html')

@app.get('/health')
def health():
    return {'status':'ok', 'model_ready': MODEL_PATH.exists()}


def load_model():
    if not MODEL_PATH.exists():
        raise HTTPException(status_code=503, detail='Model is not trained. Run: python scripts/train_model.py')
    try:
        return joblib.load(MODEL_PATH)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f'Model could not be loaded: {exc}')

@app.post('/predict')
def predict(payload: PredictionRequest):
    model = load_model()
    clinical = payload.clinical.model_dump()
    row = {k: clinical.get(k) for k in FEATURES}
    if row['age'] is None:
        raise HTTPException(status_code=422, detail='Age is required. Please provide age in the assessment.')
    if row['sex'] is None:
        raise HTTPException(status_code=422, detail='Sex is required for this trained model.')
    df = pd.DataFrame([row], columns=FEATURES)
    probability = float(model.predict_proba(df)[0][1])
    label = 'higher' if probability >= 0.5 else 'lower'
    provided = sum(v is not None for v in row.values())
    coverage = provided / len(FEATURES)
    profile = payload.profile.model_dump()
    prediction_id = save_prediction(probability, label, 'Logistic Regression', row, profile, coverage)
    return {
        'prediction_id': prediction_id,
        'risk_probability': round(probability, 4),
        'risk_label': label,
        'model': 'Logistic Regression',
        'clinical_coverage': round(coverage, 3),
        'message': 'Model-estimated cardiovascular risk. This is not a diagnosis.'
    }

@app.get('/stats')
def get_stats():
    return stats()

@app.get('/history')
def get_history():
    return recent()

@app.post('/rag')
def rag(body: dict):
    query = str(body.get('question') or body.get('query') or '').strip()

    if len(query) < 3:
        raise HTTPException(
            status_code=422,
            detail='Please enter a health question.'
        )

    retrieved = rank_chunks(query, top_k=3)
    answer, mode = ask_health_ai(query, retrieved)

    unsafe_personal = any(
        term in query.lower()
        for term in [
            'exact medication',
            'medication dose',
            'medication',
            'what dose',
            'my personal',
            'for me',
            'what should i take',
            'treatment plan',
            'prescribe'
        ]
    )

    return {
        'answer': answer,
        'mode': mode,
        'sources': retrieved,
        'knowledge_boundary': (
            unsafe_personal or
            not retrieved or
            retrieved[0]['score'] < 0.08
        )
    } 
    if len(query) < 3:
        raise HTTPException(status_code=422, detail='Please enter a health question.')
    retrieved = rank_chunks(query, top_k=3)
    answer, mode = ask_health_ai(query, retrieved)
    unsafe_personal = any(term in query.lower() for term in ['exact medication', 'medication dose', 'medication', 'what dose', 'my personal', 'for me', 'what should i take', 'treatment plan', 'prescribe'])
    return {'answer': answer, 'mode': mode, 'sources': retrieved, 'knowledge_boundary': unsafe_personal or retrieved[0]['score'] < 0.08}

@app.get('/developer/evaluation')
def developer_evaluation():
    p = ROOT / 'evaluation' / 'evaluation_results.md'
    return {'available': p.exists(), 'path': str(p)}
