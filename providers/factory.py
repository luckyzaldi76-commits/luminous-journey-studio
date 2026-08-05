from providers.openrouter import OpenRouterProvider

try:
    from providers.gemini import GeminiProvider
except ImportError:
    GeminiProvider = None


class ProviderFactory:

    @staticmethod
    def create(provider: str):

        provider = provider.lower()

        if provider == "openrouter":
            return OpenRouterProvider()

        if provider == "gemini":

            if GeminiProvider is None:
                raise RuntimeError("Gemini provider belum tersedia.")

            return GeminiProvider()

        raise ValueError(f"Unknown provider: {provider}")