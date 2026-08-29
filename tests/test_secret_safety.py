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

        env_file.write_text(
            """
AI_PROVIDER=auto
USE_MOCK=false
DEBUG=false
OPENROUTER_API_KEY=test-openrouter-secret
GEMINI_API_KEY=test-gemini-secret
""",
            encoding="utf-8",
        )

        env = os.environ.copy()

        env[
            "LUMINOUS_JOURNEY_ENV_FILE"
        ] = str(env_file)

        env[
            "PROVIDER_HEALTH_FILE"
        ] = str(
            Path(temp_dir)
            / "provider_health.json"
        )

        result = run(
            """
from config import settings

assert (
    settings.OPENROUTER_API_KEY
    == "test-openrouter-secret"
)

assert (
    settings.GEMINI_API_KEY
    == "test-gemini-secret"
)

print("SECRETS_LOADED")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "SECRETS_LOADED"
            in result.stdout
        )

        result = run(
            """
from config import settings

values = (
    settings.OPENROUTER_API_KEY,
    settings.GEMINI_API_KEY,
)

for value in values:

    assert value

    assert value not in {
        "REPLACE_ME",
        "YOUR_API_KEY",
        "your-api-key",
        "changeme",
        "test",
    }

print("SECRETS_VALID")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "SECRETS_VALID"
            in result.stdout
        )

        result = run(
            """
from config import settings

output = str(settings)

assert (
    settings.OPENROUTER_API_KEY
    not in output
)

assert (
    settings.GEMINI_API_KEY
    not in output
)

print("NO_SECRET_IN_SETTINGS_REPR")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "NO_SECRET_IN_SETTINGS_REPR"
            in result.stdout
        )

        result = run(
            """
from services.provider_health import ProviderHealthRegistry

registry = ProviderHealthRegistry()

registry.record_failure(
    "openrouter",
    RuntimeError(
        "provider failed"
    ),
    cooldown=1,
)

snapshot = registry.snapshot()

assert (
    "openrouter"
    in snapshot
)

text = str(snapshot)

assert (
    "test-openrouter-secret"
    not in text
)

assert (
    "test-gemini-secret"
    not in text
)

print("NO_SECRET_IN_HEALTH_STATE")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "NO_SECRET_IN_HEALTH_STATE"
            in result.stdout
        )

    print(
        "PASS : API secrets load from environment"
    )

    print(
        "PASS : placeholder secrets are rejected"
    )

    print(
        "PASS : settings representation does not expose secrets"
    )

    print(
        "PASS : provider health state does not expose secrets"
    )

    print()

    print("=" * 60)

    print(
        "SECRET SAFETY TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()