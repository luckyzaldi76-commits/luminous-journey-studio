from services.parser_service import ParserService


class BuilderService:

    @staticmethod
    def build(response: str) -> dict:

        sections = ParserService.parse(response)

        return {
            "title": sections.get("TITLE", ""),
            "script": sections.get("SCRIPT", ""),
            "seo": sections.get("SEO", ""),
            "hashtags": sections.get("HASHTAGS", ""),
            "metadata": sections.get("METADATA", ""),
            "image_prompts": sections.get("IMAGE_PROMPTS", ""),
        }