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
AI_PROVIDER=invalid-provider
USE_MOCK=false
DEBUG=false
""",
            encoding="utf-8",
        )

        env = os.environ.copy()

        env[
            "LUMINOUS_JOURNEY_ENV_FILE"
        ] = str(env_file)

        result = run(
            """
from config import settings

assert (
    settings.AI_PROVIDER
    == "invalid-provider"
)

assert (
    settings.USE_MOCK
    is False
)

print("CONFIG_LOAD_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "CONFIG_LOAD_OK"
            in result.stdout
        )

        result = run(
            """
from providers.factory import ProviderFactory

print(
    ProviderFactory
)

try:
    ProviderFactory.create(
        "invalid-provider"
    )
except Exception as error:

    print(
        "FACTORY_REJECTED"
    )

    print(
        type(error).__name__
    )

else:

    raise AssertionError(
        "Invalid provider was accepted"
    )
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "FACTORY_REJECTED"
            in result.stdout
        )

        result = run(
            """
from config import settings

assert (
    settings.AI_PROVIDER
    == "invalid-provider"
)

assert (
    settings.USE_MOCK
    is False
)

print("SAFE_CONFIG_STATE")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "SAFE_CONFIG_STATE"
            in result.stdout
        )

    print(
        "PASS : invalid configuration loads without crashing"
    )

    print(
        "PASS : invalid provider is rejected by factory"
    )

    print(
        "PASS : invalid configuration does not enable mock"
    )

    print()

    print("=" * 60)

    print(
        "CONFIGURATION FAILURE HANDLING TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()