import random
import time
import requests

API_URL = "http://127.0.0.1:8000"

MODE = "abnormal"   # change to "abnormal" for testing


def generate_heart_rate():
    if MODE == "normal":
        return random.randint(65, 85)

    elif MODE == "abnormal":
        return random.randint(140, 170)


while True:
    heart_rate = generate_heart_rate()

    data = {
        "heart_rate": heart_rate
    }

    try:
        response = requests.post(
            f"{API_URL}/readings",
            json=data
        )

        print(
            f"Heart Rate: {heart_rate} | "
            f"Server: {response.status_code}"
        )

    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

    time.sleep(2)