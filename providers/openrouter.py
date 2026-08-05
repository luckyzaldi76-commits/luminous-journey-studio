from providers.base import AIProvider

from services.openrouter_service import (
    generate,
    stream,
)


class OpenRouterProvider(AIProvider):

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:

        return generate(
            prompt,
            max_tokens=max_tokens,
        )

    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        return stream(
            prompt,
            max_tokens=max_tokens,
        )