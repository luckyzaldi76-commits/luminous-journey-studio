import json
from datetime import datetime


class MetadataBuilder:

    def build(
        self,
        data,
        output_file
    ):

        metadata = {

            "created_at": datetime.now().isoformat(),

            "theme": data.get(
                "THEME",
                ""
            ),

            "title": data.get(
                "TITLE",
                ""
            ),

            "scripture": data.get(
                "SCRIPTURE",
                ""
            ),

            "language": "English",

            "status": "completed"

        }

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Metadata Saved : {output_file}"
        )


builder = MetadataBuilder()