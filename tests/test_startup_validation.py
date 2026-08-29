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


def clean_env():

    env = os.environ.copy()

    for key in (
        "AI_PROVIDER",
        "USE_MOCK",
        "MOCK",
        "DEBUG",
        "REQUEST_TIMEOUT",
        "MAX_RETRY",
        "PROVIDER_HEALTH_DEFAULT_COOLDOWN",
        "PROVIDER_HEALTH_QUOTA_COOLDOWN",
        "PROVIDER_HEALTH_SERVER_COOLDOWN",
    ):

        env.pop(
            key,
            None,
        )

    return env


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
REQUEST_TIMEOUT=120
MAX_RETRY=3
PROVIDER_HEALTH_DEFAULT_COOLDOWN=60
PROVIDER_HEALTH_QUOTA_COOLDOWN=300
PROVIDER_HEALTH_SERVER_COOLDOWN=30
""",
            encoding="utf-8",
        )

        env = clean_env()

        env[
            "LUMINOUS_JOURNEY_ENV_FILE"
        ] = str(env_file)

        result = run(
            """
from config import settings

assert settings.AI_PROVIDER == "auto"
assert settings.USE_MOCK is False
assert settings.REQUEST_TIMEOUT == 120
assert settings.MAX_RETRY == 3
assert settings.PROVIDER_HEALTH_DEFAULT_COOLDOWN == 60
assert settings.PROVIDER_HEALTH_QUOTA_COOLDOWN == 300
assert settings.PROVIDER_HEALTH_SERVER_COOLDOWN == 30

print("STARTUP_CONFIG_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "STARTUP_CONFIG_OK"
            in result.stdout
        )

        env_file.write_text(
            """
AI_PROVIDER=gemini
USE_MOCK=false
DEBUG=false
REQUEST_TIMEOUT=90
MAX_RETRY=2
PROVIDER_HEALTH_DEFAULT_COOLDOWN=45
PROVIDER_HEALTH_QUOTA_COOLDOWN=240
PROVIDER_HEALTH_SERVER_COOLDOWN=20
""",
            encoding="utf-8",
        )

        result = run(
            """
from config import settings

assert settings.AI_PROVIDER == "gemini"
assert settings.USE_MOCK is False
assert settings.REQUEST_TIMEOUT == 90
assert settings.MAX_RETRY == 2
assert settings.PROVIDER_HEALTH_DEFAULT_COOLDOWN == 45
assert settings.PROVIDER_HEALTH_QUOTA_COOLDOWN == 240
assert settings.PROVIDER_HEALTH_SERVER_COOLDOWN == 20

print("RELOAD_CONFIG_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "RELOAD_CONFIG_OK"
            in result.stdout
        )

        env_file.write_text(
            """
AI_PROVIDER=auto
USE_MOCK=false
DEBUG=false
REQUEST_TIMEOUT=not-a-number
""",
            encoding="utf-8",
        )

        result = run(
            """
try:
    from config import settings
except (ValueError, TypeError):
    print("INVALID_CONFIG_REJECTED")
else:
    raise AssertionError(
        "Invalid numeric configuration was accepted"
    )
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "INVALID_CONFIG_REJECTED"
            in result.stdout
        )

    print(
        "PASS : startup configuration loads correctly"
    )

    print(
        "PASS : environment configuration is isolated"
    )

    print(
        "PASS : configuration values are applied consistently"
    )

    print(
        "PASS : invalid numeric configuration is rejected"
    )

    print()

    print("=" * 60)

    print(
        "STARTUP VALIDATION TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()