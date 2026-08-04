from config.settings import STAGE3_MAX_TOKENS
from services.ai_service import AIService


class Stage3Service:

    def __init__(self, provider="openrouter"):
        self.ai = AIService(provider)

    def generate(
        self,
        script: str,
    ) -> str:

        prompt = f"""
Based ONLY on this devotional.

{script}

Return ONLY markdown.

# IMAGE_PROMPTS

Generate exactly 10 cinematic AI image prompts.

Requirements:

- Biblical
- Photorealistic
- Netflix documentary style
- Golden hour lighting
- Ultra realistic
- 16:9 composition
- No text
- One prompt per line

Do not generate TITLE.
Do not generate SCRIPT.
Do not generate SEO.
Do not generate HASHTAGS.
Do not generate METADATA.
"""

        return self.ai.generate(
            prompt,
            max_tokens=STAGE3_MAX_TOKENS,
        )