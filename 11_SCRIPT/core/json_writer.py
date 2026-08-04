import json
from pathlib import Path

OUTPUT_FOLDER = Path(r"E:\LUMINOUS JOURNEY\04_JSON")


def save_json(reading):

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    filename = reading.date.replace("-", "") + "_IND.json"

    file_path = OUTPUT_FOLDER / filename

    data = {
        "date": reading.date,
        "language": "IND",
        "reading1": reading.reading1 or "",
        "reading2": reading.reading2 or "",
        "gospel": reading.gospel or "",
        "title": "",
        "hook": "",
        "message": [],
        "story": [],
        "reflection": [],
        "prayer": [],
        "quote": ""
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return file_path