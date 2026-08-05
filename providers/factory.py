from providers.openrouter import OpenRouterProvider
from providers.gemini import GeminiProvider


class ProviderFactory:

    @staticmethod
    def create(provider: str):

        provider = provider.lower()

        if provider == "openrouter":
            return OpenRouterProvider()

        if provider == "gemini":
            return GeminiProvider()

        raise ValueError(f"Unknown provider: {provider}")