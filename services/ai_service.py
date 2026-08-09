from providers.factory import ProviderFactory

from services.retry_policy import RetryPolicy
from services.retry_service import RetryService


class AIService:

    def __init__(
        self,
        provider_name: str,
    ):

        self.provider_name = provider_name

        self.provider = ProviderFactory.create(

            provider_name,

        )

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:

        return RetryService.execute(

            lambda: self.provider.generate(

                prompt,

                max_tokens=max_tokens,

            ),

            retry_policy=RetryPolicy,

        )

    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        def runner():

            yield from self.provider.stream(

                prompt,

                max_tokens=max_tokens,

            )

        return RetryService.execute(

            runner,

            retry_policy=RetryPolicy,

        )

    @property
    def name(
        self,
    ) -> str:

        return self.provider_name

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(provider='{self.provider_name}')"

        )