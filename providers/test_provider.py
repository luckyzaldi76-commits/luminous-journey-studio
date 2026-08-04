from providers.factory import ProviderFactory

ProviderFactory.create("openrouter")

print(type(provider).__name__)