from providers.base import AIProvider
from services.openrouter_service import generate


class OpenRouterProvider(AIProvider):

    def generate(self, prompt: str) -> str:
        return generate(prompt)