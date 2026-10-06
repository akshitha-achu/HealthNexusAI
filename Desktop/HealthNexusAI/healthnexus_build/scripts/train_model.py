from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEED = 400
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'heart.csv'
MODELS = ROOT / 'models'
MODELS.mkdir(exist_ok=True)

FEATURES = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']
TARGET = 'target'
CATEGORICAL = ['sex','cp','fbs','restecg','exang','slope','ca','thal']
NUMERIC = [c for c in FEATURES if c not in CATEGORICAL]


def load_data():
    df = pd.read_csv(DATA)
    df = df.replace('?', np.nan)
    for c in FEATURES + [TARGET]:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.dropna(subset=[TARGET]).copy()
    df[TARGET] = (df[TARGET] > 0).astype(int)
    return df


def make_preprocessor():
    num = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
    ])
    cat = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
    ])
    return ColumnTransformer([('num', num, NUMERIC), ('cat', cat, CATEGORICAL)])


def main():
    df = load_data()
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=SEED, stratify=y
    )

    results = {}
    for name, estimator in {
        'logistic_regression': LogisticRegression(max_iter=2000, random_state=SEED),
        'random_forest': RandomForestClassifier(n_estimators=300, random_state=SEED, n_jobs=-1),
    }.items():
        pipe = Pipeline([('preprocess', make_preprocessor()), ('model', estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        results[name] = {
            'accuracy': round(float(accuracy_score(y_test, pred)), 4),
            'precision': round(float(precision_score(y_test, pred, zero_division=0)), 4),
            'recall': round(float(recall_score(y_test, pred, zero_division=0)), 4),
            'f1': round(float(f1_score(y_test, pred, zero_division=0)), 4),
        }
        joblib.dump(pipe, MODELS / f'{name}.joblib')

    source_status = (DATA.parent / 'source_status.txt').read_text(encoding='utf-8').strip() if (DATA.parent / 'source_status.txt').exists() else 'UNKNOWN'
    metadata = {
        'seed': SEED,
        'usn_suffix': '0400',
        'dataset_rows': int(len(df)),
        'features': FEATURES,
        'target': TARGET,
        'test_size': 0.20,
        'metrics': results,
        'data_source_status': source_status,
        'note': 'Target is normalized to binary. If source status is DEMO_SYNTHETIC_FALLBACK_ONLY, replace data/heart.csv with the public UCI-derived CSV before submission.',
    }
    (MODELS / 'metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(json.dumps(metadata, indent=2))

if __name__ == '__main__':
    main()
