from providers.base import AIProvider
from services.gemini_service import generate


class GeminiProvider(AIProvider):

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
    ) -> str:

        return generate(prompt)