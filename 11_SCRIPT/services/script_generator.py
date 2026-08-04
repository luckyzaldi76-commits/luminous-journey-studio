from pathlib import Path
import json


def create_script(json_file):

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    script = f"""
{data.get("hook","")}

{data.get("historical_background","")}

{data.get("reflection","")}

{data.get("application","")}

{data.get("prayer","")}
""".strip()

    folder = Path("06_SCRIPT")
    folder.mkdir(exist_ok=True)

    file = folder / (Path(json_file).stem + ".txt")

    with open(file, "w", encoding="utf-8") as f:
        f.write(script)

    return file