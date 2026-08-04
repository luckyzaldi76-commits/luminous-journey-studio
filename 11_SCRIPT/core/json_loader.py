from pathlib import Path
import json


class JsonLoader:

    def load_folder(self, folder):

        folder = Path(folder)

        data = {}

        if not folder.exists():
            return data

        for file in folder.glob("*.json"):

            with open(file, "r", encoding="utf-8") as f:
                obj = json.load(f)

            data[obj["id"]] = obj

        return data