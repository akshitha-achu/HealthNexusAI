from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

client = TestClient(app)


def payload():
    return {
        'profile': {
            'medical_history': 'High cholesterol',
            'family_history': 'Parent(s)',
            'lifestyle': 'Moderately active',
            'smoking': 'Former smoker',
            'alcohol': 'Occasional',
            'sleep': '6–7 hours',
            'bmi': 23.4,
            'symptoms': 'No significant symptoms',
            'has_report': True,
        },
        'clinical': {
            'age': 52, 'sex': 1, 'cp': 1, 'trestbps': 130, 'chol': 240,
            'fbs': 0, 'restecg': 1, 'thalach': 155, 'exang': 0,
            'oldpeak': 0.8, 'slope': 2, 'ca': 0, 'thal': 2,
        }
    }


def test_predict_valid():
    init_db()
    r = client.post('/predict', json=payload())
    assert r.status_code == 200
    data = r.json()
    assert 0 <= data['risk_probability'] <= 1
    assert data['prediction_id'] >= 1


def test_stats_endpoint():
    init_db()
    client.post('/predict', json=payload())
    r = client.get('/stats')
    assert r.status_code == 200
    data = r.json()
    assert data['total_requests'] >= 1
    assert 0 <= data['average_predicted_risk'] <= 1
    assert 0 <= data['high_risk_share'] <= 1


def test_bad_input():
    bad = payload()
    bad['clinical']['age'] = 999
    r = client.post('/predict', json=bad)
    assert r.status_code == 422
