from pathlib import Path


class PromptLoader:

    @staticmethod
    def load(path: Path) -> str:

        return path.read_text(
            encoding="utf-8"
        )