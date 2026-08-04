from pathlib import Path

class BibleImporter:

    def __init__(self):
        self.resource = Path("resources/bible")
        self.dataset = Path("datasets/bible")
        self.knowledge = Path("KNOWLEDGE")

    def run(self):

        print("="*40)
        print("BIBLE IMPORTER")
        print("="*40)

        print("Resource :", self.resource)
        print("Dataset  :", self.dataset)
        print("Knowledge:", self.knowledge)

        print()
        print("READY")