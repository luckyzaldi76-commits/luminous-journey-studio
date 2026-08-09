from pathlib import Path

from config.settings import TEMPLATE_DIR


class TemplateLoader:

    TEMPLATE_DIR = TEMPLATE_DIR

    @classmethod
    def load(
        cls,
        filename: str,
        **kwargs,
    ) -> str:

        path = cls.path(
            filename,
        )

        if not path.exists():

            raise FileNotFoundError(
                f"Template not found: {path}"
            )

        template = path.read_text(
            encoding="utf-8",
        )

        try:

            return template.format(
                **kwargs,
            )

        except KeyError as error:

            raise RuntimeError(
                f"Missing template variable: "
                f"{error.args[0]}"
            ) from error

    @classmethod
    def exists(
        cls,
        filename: str,
    ) -> bool:

        return cls.path(
            filename,
        ).exists()

    @classmethod
    def path(
        cls,
        filename: str,
    ) -> Path:

        return cls.TEMPLATE_DIR / filename

    @classmethod
    def list(
        cls,
    ) -> list[str]:

        if not cls.TEMPLATE_DIR.exists():

            return []

        return sorted(
            file.name
            for file in cls.TEMPLATE_DIR.glob("*.md")
        )