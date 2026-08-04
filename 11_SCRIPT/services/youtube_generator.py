from pathlib import Path
import json


def create_youtube(json_file):

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("seo_title", "")
    description = data.get("seo_description", "")

    hashtags = (
        "#LuminousJourney\n"
        "#RenunganKatolik\n"
        "#InjilHariIni\n"
        "#MeditasiKitabSuci\n"
        "#BibleMeditation\n"
        "#Catholic\n"
        "#JesusChrist"
    )

    folder = Path("09_YOUTUBE")
    folder.mkdir(exist_ok=True)

    output = folder / (Path(json_file).stem + ".txt")

    with open(output, "w", encoding="utf-8") as f:
        f.write("YOUTUBE TITLE\n\n")
        f.write(title)
        f.write("\n\n")
        f.write("YOUTUBE DESCRIPTION\n\n")
        f.write(description)
        f.write("\n\n")
        f.write("HASHTAGS\n\n")
        f.write(hashtags)

    return output