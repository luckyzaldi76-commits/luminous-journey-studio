from providers.factory import ProviderFactory

provider = ProviderFactory.create("openrouter")

print(type(provider).__name__)python tests/test_provider.py