# Cardio AI — Fire-Boltt Edition

AI-based physiological anomaly detection using data collected from Fire-Boltt smartwatches.

## Important
This is an academic/research prototype. It does NOT diagnose heart attacks or replace a doctor.

## Architecture

Fire-Boltt Watch
    -> Bluetooth / supported Fire-Boltt companion-data path
    -> Android App
    -> Standard Health Data
    -> Python FastAPI
    -> SQLite
    -> Feature Engineering
    -> Isolation Forest anomaly model
    -> Dashboard / Alert

## Why an adapter layer?
Fire-Boltt has multiple watch families and companion applications. Bluetooth data access is not identical across every model. Therefore the Android app uses a FireBolttAdapter interface rather than assuming one universal GATT layout.

The adapter currently includes:
- a simulator/demo adapter for development
- a direct BLE adapter scaffold for models that expose readable/notify GATT characteristics
- a normalized health-data model

Before using direct BLE with a specific watch, inspect that watch's actual GATT services/characteristics and confirm that the model permits third-party access.

## Project folders

- android/      Android Kotlin app scaffold
- backend/      FastAPI + SQLite + ML
- dashboard/   Streamlit dashboard
- simulator/   Generate sample Fire-Boltt-like health data
- docs/        architecture and integration notes

## Run backend

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Run dashboard

cd dashboard
pip install -r requirements.txt
streamlit run app.py

## Generate sample data

cd simulator
pip install -r requirements.txt
python simulate.py

## Android

Open android/ in Android Studio.

The Android project is intentionally a scaffold because the exact Fire-Boltt watch model determines the GATT UUIDs and/or supported companion-health integration. Replace the adapter configuration after identifying the target model.
