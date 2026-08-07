import re


class ParserService:

    HEADERS = {
        "TITLE",
        "SCRIPT",
        "SEO",
        "HASHTAGS",
        "IMAGE_PROMPTS",
        "METADATA",
    }

    HEADER_PATTERN = re.compile(
        r"^#{1,6}\s*(.+?)\s*$",
        re.IGNORECASE,
    )

    @classmethod
    def parse(
        cls,
        text: str,
    ) -> dict:

        sections = {}

        current = None

        buffer = []

        for raw_line in text.splitlines():

            header = cls._header(raw_line)

            if header:

                if current is not None:

                    sections[current] = (
                        "\n".join(buffer).strip()
                    )

                current = header

                buffer = []

                continue

            if current is not None:

                buffer.append(raw_line)

        if current is not None:

            sections[current] = (
                "\n".join(buffer).strip()
            )

        return sections

    @classmethod
    def get(
        cls,
        text: str,
        section: str,
        default: str = "",
    ) -> str:

        return cls.parse(text).get(
            section.upper(),
            default,
        )

    @classmethod
    def title(cls, text: str):

        return cls.get(
            text,
            "TITLE",
        )

    @classmethod
    def script(cls, text: str):

        return cls.get(
            text,
            "SCRIPT",
        )

    @classmethod
    def seo(cls, text: str):

        return cls.get(
            text,
            "SEO",
        )

    @classmethod
    def hashtags(cls, text: str):

        return cls.get(
            text,
            "HASHTAGS",
        )

    @classmethod
    def image_prompts(cls, text: str):

        return cls.get(
            text,
            "IMAGE_PROMPTS",
        )

    @classmethod
    def metadata(cls, text: str):

        return cls.get(
            text,
            "METADATA",
        )

    @classmethod
    def _header(
        cls,
        line: str,
    ):

        match = cls.HEADER_PATTERN.match(
            line.strip()
        )

        if not match:

            return None

        header = (
            match.group(1)
            .strip()
            .upper()
            .replace(" ", "_")
        )

        if header in cls.HEADERS:

            return header

        return None