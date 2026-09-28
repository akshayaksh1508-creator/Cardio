# Project Plan — Fire-Boltt Cardio AI

## Goal
Build an Android + Python system that collects supported physiological measurements from a Fire-Boltt smartwatch and detects unusual patterns against a user's personal baseline.

## Measurements
Preferred:
- Heart rate
- SpO2
- HRV, if exposed by the watch/data source
- Steps/activity
- Sleep, if exposed
- Skin temperature, if exposed

## Processing
1. Timestamp incoming measurements.
2. Normalize into one JSON structure.
3. Save raw observations.
4. Create rolling-window features.
5. Learn a personal baseline.
6. Run anomaly detection.
7. Display status and trend.
8. Trigger a high-priority notification only for persistent/severe anomalous patterns.

## Safety
The system must not output "heart attack detected". Use labels such as:
- Normal pattern
- Unusual physiological pattern
- Persistent abnormal pattern
- High-priority health alert

If a person has concerning symptoms, they should seek professional/emergency medical care rather than relying on the app.
