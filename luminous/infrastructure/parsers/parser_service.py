import re


class ParserService:

    HEADERS = (
        "TITLE",
        "SCRIPT",
        "SEO",
        "HASHTAGS",
        "IMAGE_PROMPTS",
        "METADATA",
    )

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

        for line in text.splitlines():

            header = cls._header(
                line,
            )

            if header:

                if current is not None:

                    sections[current] = (
                        "\n".join(
                            buffer,
                        ).strip()
                    )

                current = header

                buffer = []

                continue

            if current is not None:

                buffer.append(
                    line,
                )

        if current is not None:

            sections[current] = (
                "\n".join(
                    buffer,
                ).strip()
            )

        return sections

    @classmethod
    def get(
        cls,
        text: str,
        section: str,
        default: str = "",
    ) -> str:

        return cls.parse(
            text,
        ).get(
            section.upper(),
            default,
        )

    @classmethod
    def title(
        cls,
        text: str,
    ) -> str:

        return cls.get(
            text,
            "TITLE",
        )

    @classmethod
    def script(
        cls,
        text: str,
    ) -> str:

        return cls.get(
            text,
            "SCRIPT",
        )

    @classmethod
    def seo(
        cls,
        text: str,
    ) -> str:

        return cls.get(
            text,
            "SEO",
        )

    @classmethod
    def hashtags(
        cls,
        text: str,
    ) -> str:

        return cls.get(
            text,
            "HASHTAGS",
        )

    @classmethod
    def image_prompts(
        cls,
        text: str,
    ) -> str:

        return cls.get(
            text,
            "IMAGE_PROMPTS",
        )

    @classmethod
    def metadata(
        cls,
        text: str,
    ) -> str:

        return cls.get(
            text,
            "METADATA",
        )

    @classmethod
    def available_sections(
        cls,
        text: str,
    ) -> tuple[str, ...]:

        return tuple(
            cls.parse(
                text,
            ).keys()
        )

    @classmethod
    def has_section(
        cls,
        text: str,
        section: str,
    ) -> bool:

        return (
            section.upper()
            in cls.parse(
                text,
            )
        )

    @classmethod
    def require(
        cls,
        text: str,
        *sections: str,
    ) -> None:

        parsed = cls.parse(
            text,
        )

        missing = [
            section
            for section in sections
            if section.upper() not in parsed
        ]

        if missing:

            raise RuntimeError(
                "Missing section(s): "
                + ", ".join(missing)
            )

    @classmethod
    def _header(
        cls,
        line: str,
    ):

        match = cls.HEADER_PATTERN.match(
            line.strip(),
        )

        if match is None:

            return None

        header = (
            match.group(1)
            .strip()
            .upper()
            .replace(
                " ",
                "_",
            )
        )

        if header in cls.HEADERS:

            return header

        return None