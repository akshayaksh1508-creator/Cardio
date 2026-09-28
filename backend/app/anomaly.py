import numpy as np
from sklearn.ensemble import IsolationForest

FEATURES = ["heart_rate", "spo2", "hrv", "temperature"]

def clean_rows(rows):
    data = []
    for row in rows:
        values = [row.get(name) for name in FEATURES]
        if any(value is not None for value in values):
            data.append([np.nan if value is None else float(value) for value in values])
    return np.asarray(data, dtype=float)

def train_and_score(rows):
    arr = clean_rows(rows)
    if len(arr) < 20:
        return {"status": "INSUFFICIENT_BASELINE", "score": None,
                "message": "Collect at least 20 valid observations before pattern scoring.",
                "model": "Isolation Forest"}
    # Impute from observed values only; entirely missing features are removed.
    keep = ~np.all(np.isnan(arr), axis=0)
    arr = arr[:, keep]
    for col_idx in range(arr.shape[1]):
        col = arr[:, col_idx]
        median = float(np.nanmedian(col))
        col[np.isnan(col)] = median
    if arr.shape[1] == 0:
        return {"status": "INSUFFICIENT_DATA", "score": None,
                "message": "No supported physiological measurements were supplied."}
    model = IsolationForest(n_estimators=150, contamination=0.05, random_state=42)
    model.fit(arr)
    scores = model.decision_function(arr)
    latest = float(scores[-1])
    status = "UNUSUAL_PATTERN" if model.predict(arr)[-1] == -1 else "NO_UNUSUAL_PATTERN"
    return {"status": status, "score": round(latest, 4),
            "message": "Exploratory anomaly score only—not a medical diagnosis.",
            "model": "Isolation Forest"}
