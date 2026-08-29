import os
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent


def run_with_env(
    overrides,
):

    with tempfile.TemporaryDirectory() as temp_dir:

        env = os.environ.copy()

        for key in (
            "AI_PROVIDER",
            "USE_MOCK",
            "MOCK",
            "DEBUG",
            "OPENROUTER_API_KEY",
            "GEMINI_API_KEY",
        ):

            env.pop(
                key,
                None,
            )

        env.update(
            overrides
        )

        env[
            "LUMINOUS_JOURNEY_ENV_FILE"
        ] = str(
            Path(temp_dir)
            / ".env"
        )

        env_file = Path(
            env[
                "LUMINOUS_JOURNEY_ENV_FILE"
            ]
        )

        env_file.write_text(
            "",
            encoding="utf-8",
        )

        return subprocess.run(
            [
                sys.executable,
                "-c",
                """
from config import settings

print(
    f"AI_PROVIDER={settings.AI_PROVIDER}"
)

print(
    f"USE_MOCK={settings.USE_MOCK}"
)
""",
            ],
            cwd=PROJECT_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )


def main():

    result = run_with_env(
        {
            "AI_PROVIDER": "auto",
            "USE_MOCK": "false",
            "MOCK": "false",
            "DEBUG": "false",
        }
    )

    assert (
        result.returncode == 0
    ), result.stderr

    assert (
        "AI_PROVIDER=auto"
        in result.stdout
    ), result.stdout

    assert (
        "USE_MOCK=False"
        in result.stdout
    ), result.stdout

    result = run_with_env(
        {
            "AI_PROVIDER": "OPENROUTER",
            "USE_MOCK": "TRUE",
            "DEBUG": "false",
        }
    )

    assert (
        result.returncode == 0
    ), result.stderr

    assert (
        "AI_PROVIDER=openrouter"
        in result.stdout
    ), result.stdout

    assert (
        "USE_MOCK=True"
        in result.stdout
    ), result.stdout

    result = run_with_env(
        {
            "AI_PROVIDER": "gemini",
            "MOCK": "1",
            "DEBUG": "false",
        }
    )

    assert (
        result.returncode == 0
    ), result.stderr

    assert (
        "AI_PROVIDER=gemini"
        in result.stdout
    ), result.stdout

    assert (
        "USE_MOCK=True"
        in result.stdout
    ), result.stdout

    result = run_with_env(
        {
            "AI_PROVIDER": "mock",
            "USE_MOCK": "yes",
            "DEBUG": "false",
        }
    )

    assert (
        result.returncode == 0
    ), result.stderr

    assert (
        "AI_PROVIDER=mock"
        in result.stdout
    ), result.stdout

    assert (
        "USE_MOCK=True"
        in result.stdout
    ), result.stdout

    print(
        "PASS : production defaults disable mock"
    )

    print(
        "PASS : provider names are normalized"
    )

    print(
        "PASS : explicit mock configuration is recognized"
    )

    print(
        "PASS : legacy MOCK configuration remains supported"
    )

    print()

    print("=" * 60)

    print(
        "ENVIRONMENT SAFETY TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()