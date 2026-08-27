from providers.factory import ProviderFactory

from services.provider_health import provider_health
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

    def _available_provider_names(self):

        return tuple(
            name
            for name in self._provider_names()
            if provider_health.available(name)
        )

    def _generate_with_provider(
        self,
        provider_name: str,
        prompt: str,
        max_tokens: int,
    ) -> str:

        provider = ProviderFactory.create(
            provider_name,
        )

        try:

            response = RetryService.execute(

                lambda: provider.generate(
                    prompt,
                    max_tokens=max_tokens,
                ),

                retry_policy=RetryPolicy,

            )

        except Exception as error:

            provider_health.record_failure(
                provider_name,
                error,
            )

            raise

        provider_health.record_success(
            provider_name,
        )

        return response

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:

        errors = []

        for provider_name in (
            self._available_provider_names()
        ):

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

        if not errors:

            raise RuntimeError(
                "All AI providers are temporarily unavailable."
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

        try:

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

        except Exception as error:

            provider_health.record_failure(
                provider_name,
                error,
            )

            raise

        provider_health.record_success(
            provider_name,
        )

    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        def runner():

            errors = []

            for provider_name in (
                self._available_provider_names()
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

            if not errors:

                raise RuntimeError(
                    "All AI stream providers are temporarily unavailable."
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