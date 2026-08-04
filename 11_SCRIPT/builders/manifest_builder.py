import json


class ManifestBuilder:

    def build(
        self,
        output_dir
    ):

        files = []

        for item in sorted(output_dir.iterdir()):

            if item.is_file():

                files.append(item.name)

        manifest = {

            "status": "success",

            "files": files

        }

        with open(
            output_dir / "manifest.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                manifest,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            "Manifest Saved :",
            output_dir / "manifest.json"
        )


builder = ManifestBuilder()