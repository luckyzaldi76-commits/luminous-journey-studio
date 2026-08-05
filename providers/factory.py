from providers.openrouter import OpenRouterProvider
from providers.gemini import GeminiProvider


class ProviderFactory:

    @staticmethod
    def create(provider_name: str):

        provider = provider_name.lower()

        if provider == "openrouter":
            return OpenRouterProvider()

        if provider == "gemini":
            return GeminiProvider()

        raise RuntimeError(
            f"Unknown AI provider: {provider_name}"
        )