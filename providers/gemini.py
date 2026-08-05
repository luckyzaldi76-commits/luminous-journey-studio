from providers.base import AIProvider

from services.gemini_service import (
    generate,
    stream,
)


class GeminiProvider(AIProvider):

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:

        return generate(prompt)

    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        return stream(prompt)