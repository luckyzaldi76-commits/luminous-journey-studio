from pathlib import Path


class PromptBuilder:

    @staticmethod
    def build(
        template: Path,
        **kwargs,
    ) -> str:

        text = template.read_text(
            encoding="utf-8"
        )

        for key, value in kwargs.items():

            text = text.replace(
                "{{" + key + "}}",
                str(value),
            )

        return text