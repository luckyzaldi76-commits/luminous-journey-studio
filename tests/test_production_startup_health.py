import os
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent.parent
)


def run(
    code: str,
    env: dict,
):

    return subprocess.run(
        [
            sys.executable,
            "-c",
            code,
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def main():

    with tempfile.TemporaryDirectory() as temp_dir:

        env_file = (
            Path(temp_dir)
            / ".env"
        )

        health_file = (
            Path(temp_dir)
            / "provider_health.json"
        )

        env_file.write_text(
            """
AI_PROVIDER=auto
USE_MOCK=false
DEBUG=false
REQUEST_TIMEOUT=120
MAX_RETRY=3
PROVIDER_HEALTH_DEFAULT_COOLDOWN=60
PROVIDER_HEALTH_QUOTA_COOLDOWN=300
PROVIDER_HEALTH_SERVER_COOLDOWN=30
""",
            encoding="utf-8",
        )

        env = os.environ.copy()

        env[
            "LUMINOUS_JOURNEY_ENV_FILE"
        ] = str(env_file)

        env[
            "PROVIDER_HEALTH_FILE"
        ] = str(health_file)

        result = run(
            """
from config import settings
from services.provider_health import (
    ProviderHealthRegistry,
)

assert settings.AI_PROVIDER == "auto"
assert settings.USE_MOCK is False

registry = ProviderHealthRegistry(
    settings.PROVIDER_HEALTH_FILE,
)

registry.clear()

snapshot = registry.snapshot()

assert snapshot == {}

print("STARTUP_HEALTH_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "STARTUP_HEALTH_OK"
            in result.stdout
        )

        result = run(
            """
from config import settings
from services.provider_health import (
    ProviderHealthRegistry,
)

registry = ProviderHealthRegistry(
    settings.PROVIDER_HEALTH_FILE,
)

registry.record_failure(
    "openrouter",
    RuntimeError(
        "503 Service Unavailable"
    ),
    cooldown=30,
)

assert (
    registry.status(
        "openrouter",
    )
    == "cooldown"
)

assert (
    registry.remaining_cooldown(
        "openrouter",
    )
    > 0
)

print("HEALTH_STATE_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "HEALTH_STATE_OK"
            in result.stdout
        )

        result = run(
            """
from config import settings
from services.provider_health import (
    ProviderHealthRegistry,
)

registry = ProviderHealthRegistry(
    settings.PROVIDER_HEALTH_FILE,
)

assert (
    registry.status(
        "openrouter",
    )
    == "cooldown"
)

assert (
    registry.available(
        "openrouter",
    )
    is False
)

registry.record_success(
    "openrouter",
)

assert (
    registry.status(
        "openrouter",
    )
    == "healthy"
)

assert (
    registry.available(
        "openrouter",
    )
    is True
)

print("RECOVERY_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "RECOVERY_OK"
            in result.stdout
        )

    print(
        "PASS : production startup loads safely"
    )

    print(
        "PASS : provider health starts empty"
    )

    print(
        "PASS : runtime health state is persisted"
    )

    print(
        "PASS : provider recovery works after startup"
    )

    print()

    print("=" * 60)

    print(
        "PRODUCTION STARTUP HEALTH TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()