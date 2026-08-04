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
Do not generate hashtags.
Do not generate image prompts.
Do not generate metadata.
"""

        return self.ai.generate(prompt)