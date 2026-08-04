from config.settings import STAGE2_MAX_TOKENS
from services.ai_service import AIService


class Stage2Service:

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

# SEO

120-160 characters.

# HASHTAGS

Exactly 10 hashtags.

Do not generate TITLE.
Do not generate SCRIPT.
Do not generate IMAGE_PROMPTS.
Do not generate METADATA.
"""

        return self.ai.generate(
            prompt,
            max_tokens=STAGE2_MAX_TOKENS,
        )