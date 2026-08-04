from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

print("API KEY :", os.getenv("OPENROUTER_API_KEY"))
print("MODEL   :", os.getenv("OPENROUTER_MODEL"))

from services.gemini_service import generate

try:
    hasil = generate("Reply only: CONNECTED")
    print("\nSUCCESS")
    print(hasil)

except Exception as e:
    print("\nERROR")
    print(e)