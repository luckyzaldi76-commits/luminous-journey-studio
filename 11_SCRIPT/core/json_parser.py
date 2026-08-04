import json
import re


def parse_ai_response(text):

    if not text:
        raise ValueError("AI response kosong.")

    text = text.strip()

    # Jika sudah JSON murni
    try:
        return json.loads(text)
    except Exception:
        pass

    # Hilangkan blok <think>...</think>
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    ).strip()

    # Ambil isi ```json ... ```
    match = re.search(
        r"```(?:json)?\s*(.*?)```",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    if match:
        text = match.group(1).strip()

    else:
        # Ambil objek JSON pertama yang ditemukan
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

    try:
        return json.loads(text)

    except Exception as e:

        print("=" * 60)
        print("JSON PARSER ERROR")
        print("=" * 60)
        print(text[:1000])

        raise e