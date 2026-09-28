# Normalized Health Data

POST /readings

Example:

{
  "device": "Fire-Boltt Demo",
  "timestamp": "2026-09-28T10:30:00Z",
  "heart_rate": 82,
  "spo2": 97,
  "hrv": 48,
  "steps": 1250,
  "activity": "walking",
  "sleep_minutes": 420,
  "temperature": 36.7
}

Any field not supported by a particular watch can be null.

The ML layer must handle missing features rather than inventing measurements.
