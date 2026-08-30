from pathlib import Path
import shutil


class AssetPipeline:

    ASSET_FILES = (
        "script.txt",
        "response.md",
        "image_prompts.md",
        "seo.json",
        "metadata.json",
        "runtime.json",
    )

    def export(
        self,
        source_dir,
        destination_dir,
    ):

        source_dir = Path(source_dir)
        destination_dir = Path(destination_dir)

        if not source_dir.exists():
            raise FileNotFoundError(
                source_dir
            )

        destination_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        exported = []

        for name in self.ASSET_FILES:

            source = source_dir / name
            destination = destination_dir / name

            if source.exists():

                shutil.copy2(
                    source,
                    destination,
                )

                exported.append(name)

        return exported
