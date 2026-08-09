from pathlib import Path


class PromptLoader:

    @staticmethod
    def load(
        prompt_file: Path,
    ) -> str:

        return prompt_file.read_text(
            encoding="utf-8",
        )