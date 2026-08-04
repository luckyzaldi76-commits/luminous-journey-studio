from providers.base import AIProvider
from services.openrouter_service import generate


class OpenRouterProvider(AIProvider):

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
    ) -> str:

        return generate(
            prompt,
            max_tokens=max_tokens,
        )