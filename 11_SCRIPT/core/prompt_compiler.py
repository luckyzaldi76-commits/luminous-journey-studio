from pathlib import Path

from config import PROMPT_DIR


class PromptCompiler:

    def __init__(self):

        self.base = PROMPT_DIR

    def load(self, filename):

        file = self.base / filename

        return file.read_text(
            encoding="utf-8"
        ).strip()

    def compile_daily(self):

        sections = [

            "01_ROLE.md",

            "02_MISSION.md",

            "03_THEOLOGY.md",

            "04_HISTORY.md",

            "05_WRITING.md",

            "06_OUTPUT.md",

            "09_QC.md"

        ]

        result = []

        for section in sections:

            result.append(
                self.load(section)
            )

        return "\n\n".join(result)


compiler = PromptCompiler()