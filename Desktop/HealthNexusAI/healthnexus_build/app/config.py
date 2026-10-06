from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / 'models' / 'logistic_regression.joblib'
DB_PATH = ROOT / 'app.db'
DOCS_PATH = ROOT / 'data' / 'health_docs'
SEED = 400

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
