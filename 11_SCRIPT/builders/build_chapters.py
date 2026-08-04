import json
from pathlib import Path

from build_books import BOOKS


folder = Path("KNOWLEDGE/02_CHAPTERS")
folder.mkdir(parents=True, exist_ok=True)


count = 0

for code, name, total in BOOKS:

    for chapter in range(1, total + 1):

        data = {

            "id": f"{code}_{chapter:02d}",

            "book": code,

            "chapter": chapter,

            "title": "",

            "summary": "",

            "historical_background": "",

            "people": [],

            "places": [],

            "events": [],

            "themes": [],

            "cross_references": [],

            "verses": []

        }

        filename = folder / f"{code}_{chapter:02d}.json"

        with open(filename, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4, ensure_ascii=False)

        count += 1

print()

print("=" * 40)

print("Chapters created :", count)

print("=" * 40)