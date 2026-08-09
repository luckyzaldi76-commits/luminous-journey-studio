import os


class FallbackService:

    def __init__(self):

        from services.ai_service import AIService

        provider_name = os.getenv(
            "AI_PROVIDER",
            "auto",
        ).strip().lower()

        use_mock = os.getenv(
            "USE_MOCK",
            "False",
        ).strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

        if use_mock:

            provider_name = "mock"

        elif provider_name == "auto":

            provider_name = "openrouter"

        self.ai = AIService(
            provider_name,
        )

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:

        return self.ai.generate(
            prompt,
            max_tokens=max_tokens,
        )

    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        yield from self.ai.stream(
            prompt,
            max_tokens=max_tokens,
        )

    @property
    def provider(
        self,
    ) -> str:

        return self.ai.name

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(provider='{self.provider}')"
        )