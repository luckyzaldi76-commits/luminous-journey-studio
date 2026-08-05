from providers.factory import ProviderFactory


class AIService:

    def __init__(self, provider_name: str):

        self.provider = ProviderFactory.create(provider_name)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:

        return self.provider.generate(
            prompt,
            max_tokens=max_tokens,
        )

    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        return self.provider.stream(
            prompt,
            max_tokens=max_tokens,
        )