"""SQLite storage for prediction history.

Every prediction (the 7 inputs plus the model output) is saved in
`predictions.db` next to this file. The table is created on first use.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

DB_FILE = Path(__file__).parent / "predictions.db"

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


def _connect():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at      TEXT    NOT NULL,
            user_email      TEXT    NOT NULL,
            N               REAL    NOT NULL,
            P               REAL    NOT NULL,
            K               REAL    NOT NULL,
            temperature     REAL    NOT NULL,
            humidity        REAL    NOT NULL,
            ph              REAL    NOT NULL,
            rainfall        REAL    NOT NULL,
            predicted_crop  TEXT    NOT NULL,
            confidence      REAL    NOT NULL,
            top3            TEXT    NOT NULL
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_predictions_user "
        "ON predictions (user_email, created_at)"
    )
    return conn


def save_prediction(user_email, values, predicted_crop, confidence, top3):
    """Store one prediction.

    `values` maps each feature to its input value; `top3` is a list of
    (crop, probability) pairs.
    """
    with _connect() as conn:
        conn.execute(
            f"""
            INSERT INTO predictions (
                created_at, user_email, {", ".join(FEATURES)},
                predicted_crop, confidence, top3
            ) VALUES ({", ".join("?" * (len(FEATURES) + 5))})
            """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_email,
                *(float(values[feature]) for feature in FEATURES),
                predicted_crop,
                float(confidence),
                json.dumps([[crop, round(float(p), 4)] for crop, p in top3]),
            ),
        )


def get_predictions(user_email):
    """All predictions of one user, newest first, as a DataFrame."""
    with _connect() as conn:
        return pd.read_sql_query(
            "SELECT * FROM predictions WHERE user_email = ? "
            "ORDER BY id DESC",
            conn,
            params=(user_email,),
        )


def clear_predictions(user_email):
    with _connect() as conn:
        conn.execute(
            "DELETE FROM predictions WHERE user_email = ?", (user_email,)
        )
