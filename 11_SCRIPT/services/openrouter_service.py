import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")

URL = "https://openrouter.ai/api/v1/chat/completions"


def generate(prompt):

    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY tidak ditemukan di file .env")

    if not MODEL:
        raise ValueError("OPENROUTER_MODEL tidak ditemukan di file .env")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Luminous Journey Studio"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    print()
    print("=" * 60)
    print("OPENROUTER")
    print("=" * 60)
    print("Model :", MODEL)

    for retry in range(5):

        print(f"Connecting... ({retry + 1}/5)")

        response = requests.post(
            URL,
            headers=headers,
            json=payload,
            timeout=300
        )

        print("Status :", response.status_code)

        if response.status_code == 200:

            print("Response received.")

            result = response.json()

            return result["choices"][0]["message"]["content"]

        if response.status_code == 429:

            print("Server Busy. Retry 10 detik...")
            time.sleep(10)
            continue

        print(response.text)
        response.raise_for_status()

    raise RuntimeError("OpenRouter gagal setelah 5 percobaan.")