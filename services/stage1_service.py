from config.settings import STAGE1_MAX_TOKENS
from services.ai_service import AIService


class Stage1Service:

    def __init__(self, provider="openrouter"):
        self.ai = AIService(provider)

    def generate(
        self,
        gospel: str,
        language: str,
        audience: str,
    ) -> str:

        prompt = f"""
Today's Gospel

{gospel}

Language

{language}

Audience

{audience}

Return ONLY markdown.

# TITLE

One title.

# SCRIPT

Maximum 700 words.

Do not generate SEO.
Do not generate HASHTAGS.
Do not generate IMAGE_PROMPTS.
Do not generate METADATA.
"""

        return self.ai.generate(
            prompt,
            max_tokens=STAGE1_MAX_TOKENS,
        )