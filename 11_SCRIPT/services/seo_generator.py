from pathlib import Path
import json


def create_seo(json_file):

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("seo_title", "")
    description = data.get("seo_description", "")

    folder = Path("08_SEO")
    folder.mkdir(exist_ok=True)

    output = folder / (Path(json_file).stem + ".txt")

    with open(output, "w", encoding="utf-8") as f:
        f.write(f"TITLE\n\n{title}\n\n")
        f.write(f"DESCRIPTION\n\n{description}")

    return output