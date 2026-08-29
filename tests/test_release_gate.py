import os
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve().parent.parent
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
OPENROUTER_API_KEY=
GEMINI_API_KEY=
""",
            encoding="utf-8",
        )

        env = os.environ.copy()

        for key in (
            "AI_PROVIDER",
            "USE_MOCK",
            "MOCK",
            "DEBUG",
            "REQUEST_TIMEOUT",
            "MAX_RETRY",
            "PROVIDER_HEALTH_FILE",
        ):

            env.pop(
                key,
                None,
            )

        env[
            "LUMINOUS_JOURNEY_ENV_FILE"
        ] = str(env_file)

        env[
            "PROVIDER_HEALTH_FILE"
        ] = str(health_file)

        result = run(
            """
from config import settings

assert (
    settings.APP_NAME
    == "Luminous Journey Studio"
)

assert settings.VERSION

assert (
    settings.AI_PROVIDER
    == "auto"
)

assert (
    settings.USE_MOCK
    is False
)

assert (
    settings.REQUEST_TIMEOUT
    == 120
)

assert (
    settings.MAX_RETRY
    == 3
)

assert (
    settings.OPENROUTER_MAX_TOKENS
    > 0
)

assert (
    len(settings.LANGUAGES)
    == 6
)

print("CONFIG_RELEASE_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "CONFIG_RELEASE_OK"
            in result.stdout
        ), result.stdout

        result = run(
            """
from services.ai_service import AIService

service = AIService("mock")

assert (
    service.name
    == "mock"
)

print("AI_SERVICE_RELEASE_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "AI_SERVICE_RELEASE_OK"
            in result.stdout
        ), result.stdout

        result = run(
            """
from services.provider_health import (
    ProviderHealthRegistry,
)

registry = ProviderHealthRegistry()

registry.clear()

assert (
    registry.snapshot()
    == {}
)

registry.record_failure(
    "mock",
    RuntimeError(
        "503 Service Unavailable"
    ),
    cooldown=1,
)

assert (
    registry.status("mock")
    == "cooldown"
)

assert (
    registry.available("mock")
    is False
)

registry.record_success(
    "mock"
)

assert (
    registry.status("mock")
    == "healthy"
)

assert (
    registry.available("mock")
    is True
)

print("HEALTH_RELEASE_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "HEALTH_RELEASE_OK"
            in result.stdout
        ), result.stdout

        result = run(
            """
from config import settings

assert (
    settings.OPENROUTER_API_KEY
    == ""
)

assert (
    settings.GEMINI_API_KEY
    == ""
)

print("SECRET_DEFAULT_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        result = run(
            """
from config import settings
from services.provider_health import (
    ProviderHealthRegistry,
)

assert (
    settings.AI_PROVIDER
    == "auto"
)

assert (
    settings.USE_MOCK
    is False
)

registry = ProviderHealthRegistry(
    settings.PROVIDER_HEALTH_FILE,
)

registry.clear()

assert (
    registry.snapshot()
    == {}
)

print("RELEASE_BOUNDARY_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "RELEASE_BOUNDARY_OK"
            in result.stdout
        ), result.stdout

    print(
        "PASS : release configuration is valid"
    )

    print(
        "PASS : AI service initializes correctly"
    )

    print(
        "PASS : provider health recovery works"
    )

    print(
        "PASS : missing API secrets remain empty"
    )

    print(
        "PASS : release environment boundary is safe"
    )

    print()

    print("=" * 60)

    print(
        "RELEASE GATE TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()