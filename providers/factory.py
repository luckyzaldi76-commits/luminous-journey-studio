from providers.gemini import GeminiProvider
from providers.openrouter import OpenRouterProvider


class ProviderFactory:

    @staticmethod
    def create(provider: str):

        provider = provider.lower()

        if provider == "gemini":
            return GeminiProvider()

        if provider == "openrouter":
            return OpenRouterProvider()

        raise ValueError(f"Unknown provider: {provider}")