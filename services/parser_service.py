import re


class ParserService:

    HEADERS = [
        "TITLE",
        "SCRIPT",
        "SEO",
        "HASHTAGS",
        "IMAGE_PROMPTS",
        "METADATA",
    ]

    @staticmethod
    def parse(text: str) -> dict:

        sections = {}

        current = None
        buffer = []

        for raw_line in text.splitlines():

            line = raw_line.rstrip()

            header = ParserService._header(line)

            if header:

                if current is not None:

                    sections[current] = "\n".join(buffer).strip()

                current = header
                buffer = []

                continue

            if current is not None:

                buffer.append(raw_line)

        if current is not None:

            sections[current] = "\n".join(buffer).strip()

        return sections

    @staticmethod
    def _header(line: str):

        line = line.strip()

        patterns = [
            r"^#\s*(.+)$",
            r"^##\s*(.+)$",
            r"^###\s*(.+)$",
        ]

        for pattern in patterns:

            match = re.match(pattern, line, re.IGNORECASE)

            if not match:
                continue

            header = (
                match.group(1)
                .strip()
                .upper()
                .replace(" ", "_")
            )

            if header in ParserService.HEADERS:

                return header

        return None