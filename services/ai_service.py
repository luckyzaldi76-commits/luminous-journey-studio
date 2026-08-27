from providers.factory import ProviderFactory

from services.retry_policy import RetryPolicy
from services.retry_service import RetryService


class AIService:

    def __init__(
        self,
        provider_name: str,
    ):

        self.provider_name = (
            provider_name.strip().lower()
        )

        self.provider = ProviderFactory.create(
            self.provider_name,
        )

    def _provider_names(self):

        names = []

        if self.provider_name:

            names.append(
                self.provider_name,
            )

        for name in (
            "openrouter",
            "gemini",
            "mock",
        ):

            if name not in names:

                names.append(
                    name,
                )

        return names

    def _generate_with_provider(
        self,
        provider_name: str,
        prompt: str,
        max_tokens: int,
    ) -> str:

        provider = ProviderFactory.create(
            provider_name,
        )

        return RetryService.execute(

            lambda: provider.generate(
                prompt,
                max_tokens=max_tokens,
            ),

            retry_policy=RetryPolicy,

        )

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:

        errors = []

        for provider_name in self._provider_names():

            try:

                response = (
                    self._generate_with_provider(
                        provider_name,
                        prompt,
                        max_tokens,
                    )
                )

                self.provider_name = provider_name

                self.provider = (
                    ProviderFactory.create(
                        provider_name,
                    )
                )

                return response

            except Exception as error:

                errors.append(
                    f"{provider_name}: {error}"
                )

        raise RuntimeError(

            "All AI providers failed: "
            + " | ".join(errors)

        )

    def _stream_with_provider(
        self,
        provider_name: str,
        prompt: str,
        max_tokens: int,
    ):

        provider = ProviderFactory.create(
            provider_name,
        )

        chunks = RetryService.execute(

            lambda: provider.stream(
                prompt,
                max_tokens=max_tokens,
            ),

            retry_policy=RetryPolicy,

        )

        yielded = False

        for chunk in chunks:

            yielded = True

            yield chunk

        if not yielded:

            raise RuntimeError(
                "Provider returned an empty stream."
            )

    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        def runner():

            errors = []

            for provider_name in (
                self._provider_names()
            ):

                try:

                    for chunk in (
                        self._stream_with_provider(
                            provider_name,
                            prompt,
                            max_tokens,
                        )
                    ):

                        yield chunk

                    self.provider_name = (
                        provider_name
                    )

                    self.provider = (
                        ProviderFactory.create(
                            provider_name,
                        )
                    )

                    return

                except Exception as error:

                    errors.append(
                        f"{provider_name}: {error}"
                    )

            raise RuntimeError(

                "All AI stream providers failed: "
                + " | ".join(errors)

            )

        return runner()

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