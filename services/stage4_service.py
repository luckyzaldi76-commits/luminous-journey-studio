from config.settings import STAGE4_MAX_TOKENS
from services.ai_service import AIService


class Stage4Service:

    def __init__(self, provider="openrouter"):
        self.ai = AIService(provider)

    def generate(
        self,
        gospel: str,
        language: str,
        audience: str,
    ) -> str:

        prompt = f"""
Return ONLY markdown.

# METADATA

AUTHOR=Luminous Journey

GOSPEL={gospel}

LANGUAGE={language}

AUDIENCE={audience}

VERSION=1.0

GENERATED_BY=Luminous Journey Studio

Do not generate anything else.
"""

        return self.ai.generate(
            prompt,
            max_tokens=STAGE4_MAX_TOKENS,
        )