"""Level 3 helper. Run manually and record the actual terminal output in question_b/level3/failure_results.md."""
from pathlib import Path
import shutil
from fastapi.testclient import TestClient
from app.main import app
from app.config import MODEL_PATH
from tests.test_app import payload

client = TestClient(app)
backup = MODEL_PATH.with_suffix('.bak')
print('--- FAILURE 1: missing model file ---')
if MODEL_PATH.exists():
    shutil.copy2(MODEL_PATH, backup)
    MODEL_PATH.unlink()
try:
    r = client.post('/predict', json=payload())
    print('status:', r.status_code)
    print('body:', r.json())
finally:
    if backup.exists():
        shutil.move(backup, MODEL_PATH)

print('\n--- FAILURE 2: invalid age ---')
bad = payload()
bad['clinical']['age'] = 999
r = client.post('/predict', json=bad)
print('status:', r.status_code)
print('body:', r.json())

print('\nFixes: model artifact restored; Pydantic range validation rejects invalid age before inference.')
