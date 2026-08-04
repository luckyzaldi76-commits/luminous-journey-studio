import json


class SEOBuilder:

    def build(
        self,
        data,
        output_file
    ):

        seo = {

            "title": data.get(
                "TITLE",
                ""
            ),

            "theme": data.get(
                "THEME",
                ""
            ),

            "description": data.get(
                "MAIN MESSAGE",
                ""
            ),

            "keywords": ""

        }

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                seo,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"SEO Saved : {output_file}")

        return output_file


builder = SEOBuilder()