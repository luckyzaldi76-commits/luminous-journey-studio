from providers.factory import ProviderFactory


class ProductionPipeline:
    def __init__(self, provider_name: str):
        self.provider = ProviderFactory.create(provider_name)

    def generate(self, prompt: str) -> str:
        return self.provider.generate(prompt)