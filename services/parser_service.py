import re


class ParserService:

    @staticmethod
    def parse(text: str) -> dict:

        sections = {}

        current = "CONTENT"

        buffer = []

        for line in text.splitlines():

            line = line.rstrip()

            match = re.match(r"^#\s+(.+)$", line)

            if match:

                sections[current] = "\n".join(buffer).strip()

                current = match.group(1).strip()

                buffer = []

                continue

            buffer.append(line)

        sections[current] = "\n".join(buffer).strip()

        return sections