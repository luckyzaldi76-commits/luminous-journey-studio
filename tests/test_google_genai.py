from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-3-flash-preview",
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

for model in MODELS:

    print("=" * 60)
    print(model)

    try:

        response = client.models.generate_content(
            model=model,
            contents="Say hello."
        )

        print("SUCCESS")
        print(response.text)
        break

    except Exception as e:

        print(type(e).__name__)
        print(e)