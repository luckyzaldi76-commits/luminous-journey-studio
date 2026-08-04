import re


def parse_markdown(text):

    data = {}

    current_key = None
    buffer = []

    lines = text.splitlines()

    for line in lines:

        line = line.rstrip()

        match = re.match(
            r"^#\s*PART\s*\d+\s*[—-]\s*(.+)$",
            line,
            flags=re.IGNORECASE,
        )

        if match:

            if current_key:

                data[current_key] = "\n".join(buffer).strip()

            current_key = match.group(1).strip().upper()

            buffer = []

        else:

            if current_key:

                buffer.append(line)

    if current_key:

        data[current_key] = "\n".join(buffer).strip()

    return data