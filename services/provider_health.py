from dataclasses import dataclass, field
from pathlib import Path
from time import monotonic, time
from threading import RLock
import json
import os
import tempfile


STATE_FILE = Path(
    os.getenv(
        "PROVIDER_HEALTH_FILE",
        "config/provider_health.json",
    )
)


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
        self.last_error = str(error)

        if cooldown is None:

            cooldown = self._cooldown_for(
                error,
            )

        self.disabled_until = (
            monotonic()
            + cooldown
        )

    def _cooldown_for(
        self,
        error: Exception,
    ) -> int:

        message = str(
            error
        ).lower()

        if any(
            item in message
            for item in (
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
            )
        ):

            return self._QUOTA_COOLDOWN

        if any(
            item in message
            for item in (
                "408",
                "409",
                "425",
                "500",
                "502",
                "503",
                "504",
                "timeout",
                "timed out",
                "connection",
                "connection reset",
                "connection aborted",
                "temporarily",
                "temporary",
                "unavailable",
                "internal server error",
                "bad gateway",
                "gateway timeout",
            )
        ):

            return self._SERVER_COOLDOWN

        return self._DEFAULT_COOLDOWN

    def is_available(
        self,
    ) -> bool:

        return (
            monotonic()
            >= self.disabled_until
        )

    def status(
        self,
    ) -> str:

        if self.is_available():

            if self.failures == 0:

                return "healthy"

            return "available"

        return "cooldown"

    def remaining_cooldown(
        self,
    ) -> float:

        return max(
            0.0,
            self.disabled_until
            - monotonic(),
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
        state_file: Path | str = STATE_FILE,
    ):

        self.state_file = Path(
            state_file,
        )

        self._providers: dict[
            str,
            ProviderHealth,
        ] = {}

        self._lock = RLock()

        self._load()

    def _remaining_cooldown(
        self,
        disabled_until: float,
    ) -> float:

        return max(
            0.0,
            disabled_until
            - monotonic(),
        )

    def _load(
        self,
    ):

        with self._lock:

            self._providers.clear()

            if not self.state_file.exists():

                return

            try:

                data = json.loads(
                    self.state_file.read_text(
                        encoding="utf-8",
                    )
                )

            except (
                OSError,
                ValueError,
                TypeError,
            ):

                return

            if not isinstance(
                data,
                dict,
            ):

                return

            saved_at = data.get(
                "saved_at",
            )

            providers = data.get(
                "providers",
                {},
            )

            if not isinstance(
                providers,
                dict,
            ):

                return

            elapsed = 0.0

            if isinstance(
                saved_at,
                (int, float),
            ):

                elapsed = max(
                    0.0,
                    time() - saved_at,
                )

            for name, value in providers.items():

                if not isinstance(
                    name,
                    str,
                ):

                    continue

                if not isinstance(
                    value,
                    dict,
                ):

                    continue

                failures = value.get(
                    "failures",
                    0,
                )

                last_error = value.get(
                    "last_error",
                    "",
                )

                remaining = value.get(
                    "remaining_cooldown",
                    0,
                )

                if not isinstance(
                    failures,
                    int,
                ):

                    failures = 0

                if not isinstance(
                    last_error,
                    str,
                ):

                    last_error = ""

                if not isinstance(
                    remaining,
                    (int, float),
                ):

                    remaining = 0.0

                remaining = max(
                    0.0,
                    float(remaining)
                    - elapsed,
                )

                self._providers[
                    name.strip().lower()
                ] = ProviderHealth(
                    failures=failures,
                    last_error=last_error,
                    disabled_until=(
                        monotonic()
                        + remaining
                        if remaining > 0
                        else 0.0
                    ),
                )

    def _save(
        self,
    ):

        with self._lock:

            try:

                self.state_file.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                payload = {
                    "saved_at": time(),
                    "providers": {
                        name: {
                            "failures": health.failures,
                            "last_error": health.last_error,
                            "remaining_cooldown": (
                                self._remaining_cooldown(
                                    health.disabled_until,
                                )
                            ),
                        }
                        for name, health
                        in self._providers.items()
                    },
                }

                fd, temp_name = tempfile.mkstemp(
                    prefix=".provider_health_",
                    suffix=".tmp",
                    dir=self.state_file.parent,
                    text=True,
                )

                try:

                    with os.fdopen(
                        fd,
                        "w",
                        encoding="utf-8",
                    ) as handle:

                        json.dump(
                            payload,
                            handle,
                            indent=2,
                        )

                    os.replace(
                        temp_name,
                        self.state_file,
                    )

                finally:

                    if os.path.exists(
                        temp_name,
                    ):

                        os.remove(
                            temp_name,
                        )

            except OSError:

                pass

    def get(
        self,
        provider_name: str,
    ) -> ProviderHealth:

        with self._lock:

            name = provider_name.strip().lower()

            if name not in self._providers:

                self._providers[
                    name
                ] = ProviderHealth()

            return self._providers[
                name
            ]

    def available(
        self,
        provider_name: str,
    ) -> bool:

        with self._lock:

            return self.get(
                provider_name,
            ).is_available()

    def status(
        self,
        provider_name: str,
    ) -> str:

        with self._lock:

            return self.get(
                provider_name,
            ).status()

    def remaining_cooldown(
        self,
        provider_name: str,
    ) -> float:

        with self._lock:

            return self.get(
                provider_name,
            ).remaining_cooldown()

    def record_success(
        self,
        provider_name: str,
    ):

        with self._lock:

            self.get(
                provider_name,
            ).record_success()

            self._save()

    def record_failure(
        self,
        provider_name: str,
        error: Exception,
        cooldown: int | None = None,
    ):

        with self._lock:

            self.get(
                provider_name,
            ).record_failure(
                error,
                cooldown,
            )

            self._save()

    def reset(
        self,
        provider_name: str,
    ):

        with self._lock:

            self.get(
                provider_name,
            ).reset()

            self._save()

    def clear(
        self,
    ):

        with self._lock:

            self._providers.clear()

            self._save()

    def reload(
        self,
    ):

        with self._lock:

            self._load()

    def snapshot(
        self,
    ) -> dict:

        with self._lock:

            return {
                name: {
                    "status": health.status(),
                    "failures": health.failures,
                    "last_error": health.last_error,
                    "available": health.is_available(),
                    "remaining_cooldown": (
                        health.remaining_cooldown()
                    ),
                }
                for name, health
                in self._providers.items()
            }


provider_health = ProviderHealthRegistry()