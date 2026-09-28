"""Send clearly labeled synthetic demo data to the local Cardio API."""
import argparse
import random
import time
from datetime import datetime, timezone

import requests

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://127.0.0.1:8000")
parser.add_argument("--mode", choices=["normal", "unusual", "alternate"], default="alternate")
parser.add_argument("--interval", type=float, default=2.0)
parser.add_argument("--count", type=int, default=0, help="0 runs until Ctrl+C")
args = parser.parse_args()
session = requests.Session()

def make_reading(index):
    mode = args.mode
    if mode == "alternate":
        mode = "normal" if (index // 20) % 2 == 0 else "unusual"
    if mode == "normal":
        hr, spo2, hrv = random.randint(62, 92), random.randint(95, 99), random.randint(30, 85)
    else:
        hr, spo2, hrv = random.randint(125, 165), random.randint(88, 94), random.randint(10, 25)
    return {
        "device": f"SIMULATED-{mode.upper()}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "heart_rate": hr, "spo2": spo2, "hrv": hrv,
        "steps": random.randint(0, 9000), "activity": "demo",
        "temperature": round(random.uniform(36.1, 37.5), 1)
    }

i = 0
try:
    while args.count == 0 or i < args.count:
        data = make_reading(i)
        try:
            response = session.post(f"{args.url.rstrip('/')}/readings", json=data, timeout=5)
            response.raise_for_status()
            print(f"#{i+1} {data['device']} HR={data['heart_rate']} SpO2={data['spo2']}% -> saved")
        except requests.RequestException as exc:
            print(f"API error: {exc}")
        i += 1
        time.sleep(max(0.2, args.interval))
except KeyboardInterrupt:
    print("\nSimulator stopped.")
