from pathlib import Path


class TemplateLoader:

    TEMPLATE_DIR = Path("templates")

    @classmethod
    def load(
        cls,
        filename: str,
        **kwargs,
    ) -> str:

        path = cls.TEMPLATE_DIR / filename

        if not path.exists():

            raise FileNotFoundError(
                f"Template not found: {path}"
            )

        text = path.read_text(
            encoding="utf-8",
        )

        return text.format(**kwargs)