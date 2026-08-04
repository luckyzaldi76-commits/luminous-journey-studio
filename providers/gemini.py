from providers.base import AIProvider
from services.gemini_service import generate


class GeminiProvider(AIProvider):

    def generate(self, prompt: str) -> str:
        return generate(prompt)