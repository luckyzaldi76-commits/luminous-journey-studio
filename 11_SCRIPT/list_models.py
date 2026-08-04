import requests

response = requests.get("https://openrouter.ai/api/v1/models")

response.raise_for_status()

for model in response.json()["data"]:
    if ":free" in model["id"]:
        print(model["id"])