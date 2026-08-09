import json
from pathlib import Path


class ExporterService:

    @classmethod
    def export(
        cls,
        output_dir: Path,
        data: dict,
    ):

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        cls._write_text(
            output_dir / "script.txt",
            data["script"],
        )

        cls._write_text(
            output_dir / "response.md",
            data["script"],
        )

        cls._write_text(
            output_dir / "image_prompts.md",
            data["image_prompts"],
        )

        cls._write_json(
            output_dir / "seo.json",
            {
                "title": data["title"],
                "seo": data["seo"],
                "hashtags": data["hashtags"],
            },
        )

        metadata = data["metadata"]

        if not isinstance(
            metadata,
            dict,
        ):

            metadata = {
                "metadata": metadata,
            }

        cls._write_json(
            output_dir / "metadata.json",
            metadata,
        )

        if "_runtime" in data:

            cls._write_json(
                output_dir / "runtime.json",
                data["_runtime"],
            )

    @staticmethod
    def _write_text(
        path: Path,
        content: str,
    ):

        path.write_text(
            content,
            encoding="utf-8",
        )

    @staticmethod
    def _write_json(
        path: Path,
        content: dict,
    ):

        path.write_text(
            json.dumps(
                content,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )