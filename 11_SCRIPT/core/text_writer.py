from pathlib import Path

TEMP = Path(r"E:\LUMINOUS JOURNEY\09_TEMP")


def save_prompt(text, filename):

    TEMP.mkdir(parents=True, exist_ok=True)

    file = TEMP / filename

    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

    return file