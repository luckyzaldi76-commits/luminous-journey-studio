from providers.base import AIProvider

from luminous.infrastructure.ai.openrouter_service import (
    generate,
    stream,
)


class OpenRouterProvider(AIProvider):

    name = "openrouter"

    @property
    def model(
        self,
    ) -> str:

        return "openrouter"

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

        yield from stream(
            prompt,
            max_tokens=max_tokens,
        )

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', "
            f"model='{self.model}')"
        )