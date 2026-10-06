from pathlib import Path
import urllib.request
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'heart.csv'
DATA.parent.mkdir(parents=True, exist_ok=True)

OFFICIAL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data'
MIRROR = 'https://raw.githubusercontent.com/sachin365123/CSV-files-for-Data-Science-and-Machine-Learning/main/heart.csv'
COLS = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','target']

if DATA.exists() and DATA.stat().st_size > 1000:
    print(f'Already present: {DATA}')
    raise SystemExit(0)

try:
    print('Downloading official UCI Cleveland data...')
    raw = ROOT / 'data' / 'processed.cleveland.data'
    urllib.request.urlretrieve(OFFICIAL, raw)
    df = pd.read_csv(raw, header=None, names=COLS, na_values='?')
    # Convert UCI's 1-based categorical codes to the 0-based UI/model codes used here.
    df['cp'] = pd.to_numeric(df['cp'], errors='coerce') - 1
    df['slope'] = pd.to_numeric(df['slope'], errors='coerce') - 1
    df['thal'] = pd.to_numeric(df['thal'], errors='coerce').map({3:1, 6:2, 7:3})
    df['target'] = (pd.to_numeric(df['target'], errors='coerce') > 0).astype(int)
    df.to_csv(DATA, index=False)
    (DATA.parent / 'source_status.txt').write_text('PUBLIC_UCI_OFFICIAL_CLEVELAND\n', encoding='utf-8')
    raw.unlink(missing_ok=True)
    print(f'Saved official UCI-derived CSV: {DATA}')
    raise SystemExit(0)
except Exception as official_error:
    print('Official UCI download failed:', official_error)

try:
    print('Trying public UCI-derived mirror...')
    raw = ROOT / 'data' / 'mirror.csv'
    urllib.request.urlretrieve(MIRROR, raw)
    df = pd.read_csv(raw)
    df.to_csv(DATA, index=False)
    (DATA.parent / 'source_status.txt').write_text('PUBLIC_UCI_DERIVED_MIRROR\n', encoding='utf-8')
    raw.unlink(missing_ok=True)
    print(f'Saved public mirror: {DATA}')
    raise SystemExit(0)
except Exception as mirror_error:
    print('Mirror download failed:', mirror_error)

# Smoke-test fallback only. Never describe this as the assignment dataset.
rng = np.random.default_rng(400)
n = 320
age = rng.integers(29, 78, n); sex = rng.integers(0, 2, n); cp = rng.integers(0, 4, n)
trestbps = np.clip(rng.normal(132, 18, n).round(), 90, 210); chol = np.clip(rng.normal(245, 48, n).round(), 130, 430)
fbs = (rng.random(n) < 0.15).astype(int); restecg = rng.integers(0, 3, n)
thalach = np.clip((205 - age + rng.normal(0, 18, n)).round(), 75, 210); exang = (rng.random(n) < 0.33).astype(int)
oldpeak = np.clip(rng.normal(1.0, 1.1, n), 0, 6).round(1); slope = rng.integers(0, 3, n); ca = rng.integers(0, 4, n); thal = rng.integers(0, 4, n)
score = (-2.5 + 0.035*(age-50) + 0.012*(trestbps-120) + 0.006*(chol-200) + .45*exang + .55*oldpeak + .55*ca + .35*(thal==3) + .25*sex + .35*(cp==0))
prob = 1/(1+np.exp(-score)); target = (rng.random(n) < prob).astype(int)
df = pd.DataFrame({'age':age,'sex':sex,'cp':cp,'trestbps':trestbps,'chol':chol,'fbs':fbs,'restecg':restecg,'thalach':thalach,'exang':exang,'oldpeak':oldpeak,'slope':slope,'ca':ca,'thal':thal,'target':target})
df.to_csv(DATA, index=False)
(DATA.parent / 'source_status.txt').write_text('DEMO_SYNTHETIC_FALLBACK_ONLY\n', encoding='utf-8')
print(f'WARNING: generated DEMO fallback at {DATA}. Do NOT submit it as the assignment dataset.')
