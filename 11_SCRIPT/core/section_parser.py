import re


class SectionParser:

    def parse(self, text):

        sections = {}

        pattern = r"##\s*(PART.*?)(?=\n##|\Z)"

        matches = re.findall(
            pattern,
            text,
            flags=re.S
        )

        for item in matches:

            lines = item.splitlines()

            title = lines[0].strip()

            body = "\n".join(lines[1:]).strip()

            sections[title] = body

        return sections


parser = SectionParser()