import numpy as np
from sklearn.ensemble import IsolationForest

FEATURES = [
    "heart_rate",
    "spo2",
    "hrv",
    "temperature",
]

def clean_rows(rows):
    values = []
    for r in rows:
        # Conservative defaults are used only for model development.
        # Production should use a model trained specifically for missingness.
        values.append([
            r.get("heart_rate"),
            r.get("spo2"),
            r.get("hrv"),
            r.get("temperature"),
        ])
    arr = np.array(values, dtype=float)
    return arr

def train_and_score(rows):
    if len(rows) < 20:
        return {
            "status": "INSUFFICIENT_BASELINE",
            "score": None,
            "message": "Collect more baseline readings before anomaly scoring."
        }

    arr = clean_rows(rows)

    # Median imputation for this prototype.
    for c in range(arr.shape[1]):
        col = arr[:, c]
        valid = col[~np.isnan(col)]
        median = float(np.median(valid)) if len(valid) else 0.0
        col[np.isnan(col)] = median
        arr[:, c] = col

    model = IsolationForest(
        n_estimators=150,
        contamination=0.05,
        random_state=42
    )
    model.fit(arr)

    scores = model.decision_function(arr)
    latest = float(scores[-1])

    if latest < -0.10:
        status = "HIGH_PRIORITY_PATTERN"
    elif latest < 0:
        status = "UNUSUAL_PATTERN"
    else:
        status = "NORMAL_PATTERN"

    return {
        "status": status,
        "score": latest,
        "message": "Physiological anomaly score; not a medical diagnosis."
    }
