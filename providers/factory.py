from providers.gemini import GeminiProvider
from providers.openrouter import OpenRouterProvider
from providers.mock import MockProvider


class ProviderFactory:

    _providers = {
        "gemini": GeminiProvider,
        "openrouter": OpenRouterProvider,
        "mock": MockProvider,
    }

    @classmethod
    def register(
        cls,
        name: str,
        provider,
    ):

        key = name.strip().lower()

        if key in cls._providers:

            raise RuntimeError(
                f"Provider '{name}' already registered."
            )

        cls._providers[key] = provider

    @classmethod
    def unregister(
        cls,
        name: str,
    ):

        cls._providers.pop(
            name.strip().lower(),
            None,
        )

    @classmethod
    def create(
        cls,
        provider_name: str,
    ):

        key = provider_name.strip().lower()

        provider = cls._providers.get(
            key,
        )

        if provider is None:

            available = ", ".join(
                cls.available(),
            )

            raise RuntimeError(
                f"Unknown AI provider '{provider_name}'. "
                f"Available providers: {available}"
            )

        return provider()

    @classmethod
    def get(
        cls,
        name: str,
    ):

        return cls._providers.get(
            name.strip().lower(),
        )

    @classmethod
    def exists(
        cls,
        name: str,
    ) -> bool:

        return (
            name.strip().lower()
            in cls._providers
        )

    @classmethod
    def available(
        cls,
    ) -> list[str]:

        return sorted(
            cls._providers.keys(),
        )

    @classmethod
    def clear(
        cls,
    ):

        cls._providers.clear()