from providers.gemini import GeminiProvider
from providers.openrouter import OpenRouterProvider


class ProviderFactory:

    _providers = {

        "gemini": GeminiProvider,

        "openrouter": OpenRouterProvider,

    }

    @classmethod
    def register(
        cls,
        name: str,
        provider,
    ):

        cls._providers[name.lower()] = provider

    @classmethod
    def create(
        cls,
        provider_name: str,
    ):

        provider = cls._providers.get(
            provider_name.lower(),
        )

        if provider is None:

            raise RuntimeError(
                f"Unknown AI provider: {provider_name}"
            )

        return provider()

    @classmethod
    def available(cls):

        return sorted(
            cls._providers.keys(),
        )