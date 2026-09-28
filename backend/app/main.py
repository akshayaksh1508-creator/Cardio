from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from .models import Reading
from .anomaly import train_and_score

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cardio AI - Fire-Boltt Backend")

class HealthReading(BaseModel):
    device: str = "Fire-Boltt"
    timestamp: datetime
    heart_rate: Optional[float] = None
    spo2: Optional[float] = None
    hrv: Optional[float] = None
    steps: Optional[int] = None
    activity: Optional[str] = None
    sleep_minutes: Optional[int] = None
    temperature: Optional[float] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {
        "project": "Cardio AI - Fire-Boltt Edition",
        "status": "running"
    }

@app.post("/readings")
def add_reading(payload: HealthReading, db: Session = Depends(get_db)):
    item = Reading(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "message": "Reading stored"}

@app.get("/readings")
def get_readings(limit: int = 200, db: Session = Depends(get_db)):
    rows = (
        db.query(Reading)
        .order_by(Reading.timestamp.desc())
        .limit(limit)
        .all()
    )
    return rows

@app.get("/anomaly")
def anomaly(db: Session = Depends(get_db)):
    rows = (
        db.query(Reading)
        .order_by(Reading.timestamp.asc())
        .all()
    )

    payload = [
        {
            "heart_rate": r.heart_rate,
            "spo2": r.spo2,
            "hrv": r.hrv,
            "temperature": r.temperature
        }
        for r in rows
    ]

    return train_and_score(payload)
