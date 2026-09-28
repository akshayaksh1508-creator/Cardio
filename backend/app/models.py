from sqlalchemy import Column, Integer, Float, String, DateTime
from .db import Base

class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    device = Column(String, default="Fire-Boltt")
    timestamp = Column(DateTime, nullable=False)
    heart_rate = Column(Float, nullable=True)
    spo2 = Column(Float, nullable=True)
    hrv = Column(Float, nullable=True)
    steps = Column(Integer, nullable=True)
    activity = Column(String, nullable=True)
    sleep_minutes = Column(Integer, nullable=True)
    temperature = Column(Float, nullable=True)
