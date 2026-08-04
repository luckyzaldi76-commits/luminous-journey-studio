import json
from pathlib import Path


class ExporterService:

    @staticmethod
    def export(output_dir: Path, data: dict):

        output_dir.mkdir(parents=True, exist_ok=True)

        (output_dir / "script.txt").write_text(
            data["script"],
            encoding="utf-8",
        )

        (output_dir / "response.md").write_text(
            data["script"],
            encoding="utf-8",
        )

        (output_dir / "seo.json").write_text(
            json.dumps(
                {
                    "title": data["title"],
                    "seo": data["seo"],
                    "hashtags": data["hashtags"],
                },
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        (output_dir / "metadata.json").write_text(
            json.dumps(
                {
                    "metadata": data["metadata"],
                },
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        (output_dir / "image_prompts.md").write_text(
            data["image_prompts"],
            encoding="utf-8",
        )