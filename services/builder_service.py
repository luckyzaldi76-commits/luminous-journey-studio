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

        for item in BuilderService.REQUIRED:
            sections.setdefault(item, "")

        return {
            "title": sections["TITLE"],
            "script": sections["SCRIPT"],
            "seo": sections["SEO"],
            "hashtags": sections["HASHTAGS"],
            "image_prompts": sections["IMAGE_PROMPTS"],
            "metadata": sections["METADATA"],
        }