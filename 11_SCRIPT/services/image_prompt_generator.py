from pathlib import Path
import json


def create_image_prompt(json_file):

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    prompt = data.get("image_prompt", "")

    folder = Path("07_IMAGE_PROMPTS")
    folder.mkdir(exist_ok=True)

    file = folder / (Path(json_file).stem + ".txt")

    with open(file, "w", encoding="utf-8") as f:
        f.write(prompt)

    return file