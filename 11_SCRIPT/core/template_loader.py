from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_template(filename):

    file = BASE_DIR / filename

    if not file.exists():
        raise FileNotFoundError(file)

    with open(file, "r", encoding="utf-8") as f:
        return f.read()