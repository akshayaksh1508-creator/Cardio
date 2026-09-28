from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from .models import Reading
from .anomaly import train_and_score

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Cardio AI API", version="1.0.0",
              description="Academic wellness-pattern prototype; not a diagnostic device.")

class HealthReading(BaseModel):
    model_config = ConfigDict(extra="forbid")
    device: str = Field(default="Cardio Demo", min_length=1, max_length=80)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    heart_rate: Optional[float] = Field(default=None, ge=20, le=250)
    spo2: Optional[float] = Field(default=None, ge=50, le=100)
    hrv: Optional[float] = Field(default=None, ge=0, le=300)
    steps: Optional[int] = Field(default=None, ge=0, le=200000)
    activity: Optional[str] = Field(default=None, max_length=80)
    sleep_minutes: Optional[int] = Field(default=None, ge=0, le=1440)
    temperature: Optional[float] = Field(default=None, ge=25, le=45)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"project": "Cardio AI", "status": "running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/readings", status_code=201)
def add_reading(payload: HealthReading, db: Session = Depends(get_db)):
    if all(getattr(payload, field) is None for field in
           ("heart_rate", "spo2", "hrv", "steps", "activity", "sleep_minutes", "temperature")):
        raise HTTPException(status_code=422, detail="At least one measurement is required.")
    item = Reading(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "message": "Reading stored", "timestamp": item.timestamp}

@app.get("/readings")
def get_readings(limit: int = Query(default=200, ge=1, le=5000),
                 db: Session = Depends(get_db)):
    return (db.query(Reading).order_by(Reading.timestamp.desc())
            .limit(limit).all())

@app.get("/anomaly")
def anomaly(db: Session = Depends(get_db)):
    rows = (db.query(Reading).order_by(Reading.timestamp.asc()).all())
    payload = [{"heart_rate": r.heart_rate, "spo2": r.spo2,
                "hrv": r.hrv, "temperature": r.temperature}
               for r in rows]
    result = train_and_score(payload)
    result["readings_used"] = len(rows)
    return result
