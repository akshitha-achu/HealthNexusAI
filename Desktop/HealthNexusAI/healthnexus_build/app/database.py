import json
import sqlite3
from pathlib import Path
from .config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            risk_probability REAL NOT NULL,
            risk_label TEXT NOT NULL,
            model_name TEXT NOT NULL,
            inputs_json TEXT NOT NULL,
            profile_json TEXT NOT NULL,
            clinical_coverage REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_prediction(risk_probability, risk_label, model_name, inputs, profile, clinical_coverage):
    conn = get_connection()
    cur = conn.execute(
        'INSERT INTO predictions (risk_probability, risk_label, model_name, inputs_json, profile_json, clinical_coverage) VALUES (?, ?, ?, ?, ?, ?)',
        (risk_probability, risk_label, model_name, json.dumps(inputs), json.dumps(profile), clinical_coverage),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def stats():
    conn = get_connection()
    row = conn.execute('''
        SELECT
            COUNT(*) AS total_requests,
            COALESCE(AVG(risk_probability), 0) AS average_predicted_risk,
            COALESCE(AVG(CASE WHEN risk_label = 'higher' THEN 1.0 ELSE 0.0 END), 0) AS high_risk_share
        FROM predictions
    ''').fetchone()
    conn.close()
    return dict(row)


def recent(limit=10):
    conn = get_connection()
    rows = conn.execute('SELECT id, created_at, risk_probability, risk_label, clinical_coverage FROM predictions ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
