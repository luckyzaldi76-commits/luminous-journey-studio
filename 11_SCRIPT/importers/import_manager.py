from pathlib import Path
import json


class ImportManager:

    def __init__(self):

        self.resources = Path("resources")
        self.datasets = Path("datasets")
        self.knowledge = Path("KNOWLEDGE")

    def prepare(self):

        folders = [

            "bible",
            "people",
            "places",
            "events",
            "themes",
            "catechism",
            "saints",
            "liturgy"

        ]

        for folder in folders:

            (self.resources / folder).mkdir(parents=True, exist_ok=True)
            (self.datasets / folder).mkdir(parents=True, exist_ok=True)

        print("=" * 50)
        print("LUMINOUS JOURNEY IMPORT ENGINE")
        print("=" * 50)

        print()

        print("Resources :", self.resources)
        print("Datasets  :", self.datasets)
        print("Knowledge :", self.knowledge)

        print()

        print("READY")


if __name__ == "__main__":

    ImportManager().prepare()