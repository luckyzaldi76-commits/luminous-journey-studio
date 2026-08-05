from services.parser_service import ParserService


class BuilderService:

    REQUIRED = [
        "TITLE",
        "SCRIPT",
        "SEO",
        "HASHTAGS",
        "IMAGE_PROMPTS",
        "METADATA",
    ]

    @staticmethod
    def build(response: str) -> dict:

        sections = ParserService.parse(response)

        data = {}

        for key in BuilderService.REQUIRED:

            value = sections.get(key, "")

            if value is None:
                value = ""

            data[key] = value.strip()

        return {
            "title": data["TITLE"],
            "script": data["SCRIPT"],
            "seo": data["SEO"],
            "hashtags": data["HASHTAGS"],
            "image_prompts": data["IMAGE_PROMPTS"],
            "metadata": data["METADATA"],
        }