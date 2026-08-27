from dataclasses import dataclass, field
from time import monotonic

from services.retry_policy import RetryPolicy


@dataclass
class ProviderHealth:

    failures: int = 0

    last_error: str = ""

    disabled_until: float = 0.0

    _DEFAULT_COOLDOWN: int = field(
        default=60,
        repr=False,
    )

    _QUOTA_COOLDOWN: int = field(
        default=300,
        repr=False,
    )

    _SERVER_COOLDOWN: int = field(
        default=30,
        repr=False,
    )

    def _cooldown_for(
        self,
        error: Exception,
    ) -> int:

        message = str(
            error
        ).lower()

        for item in RetryPolicy.NO_RETRY:

            if item in message:

                if item in {
                    "401",
                    "402",
                    "403",
                    "429",
                    "quota",
                    "resource_exhausted",
                    "insufficient",
                    "credit",
                    "invalid api key",
                    "invalid_api_key",
                    "unauthorized",
                    "permission",
                    "forbidden",
                }:

                    return self._QUOTA_COOLDOWN

                return self._DEFAULT_COOLDOWN

        for item in RetryPolicy.RETRY:

            if item in message:

                return self._SERVER_COOLDOWN

        return self._DEFAULT_COOLDOWN

    def record_success(
        self,
    ):

        self.failures = 0

        self.last_error = ""

        self.disabled_until = 0.0

    def record_failure(
        self,
        error: Exception,
        cooldown: int | None = None,
    ):

        self.failures += 1

        self.last_error = str(
            error,
        )

        if cooldown is None:

            cooldown = self._cooldown_for(
                error,
            )

        self.disabled_until = (
            monotonic()
            + cooldown
        )

    def is_available(
        self,
    ) -> bool:

        return (
            monotonic()
            >= self.disabled_until
        )

    def reset(
        self,
    ):

        self.failures = 0

        self.last_error = ""

        self.disabled_until = 0.0


class ProviderHealthRegistry:

    def __init__(
        self,
    ):

        self._providers: dict[
            str,
            ProviderHealth,
        ] = {}

    def get(
        self,
        provider_name: str,
    ) -> ProviderHealth:

        name = provider_name.strip().lower()

        if name not in self._providers:

            self._providers[name] = (
                ProviderHealth()
            )

        return self._providers[name]

    def available(
        self,
        provider_name: str,
    ) -> bool:

        return self.get(
            provider_name,
        ).is_available()

    def record_success(
        self,
        provider_name: str,
    ):

        self.get(
            provider_name,
        ).record_success()

    def record_failure(
        self,
        provider_name: str,
        error: Exception,
        cooldown: int | None = None,
    ):

        self.get(
            provider_name,
        ).record_failure(
            error,
            cooldown,
        )

    def reset(
        self,
        provider_name: str,
    ):

        self.get(
            provider_name,
        ).reset()

    def clear(
        self,
    ):

        self._providers.clear()

    def snapshot(
        self,
    ) -> dict:

        return {
            name: {
                "failures": health.failures,
                "last_error": health.last_error,
                "available": health.is_available(),
            }
            for name, health
            in self._providers.items()
        }


provider_health = ProviderHealthRegistry()