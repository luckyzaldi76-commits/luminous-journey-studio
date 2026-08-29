import os
import subprocess
import sys
import tempfile
from pathlib import Path


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
        env=env,
        capture_output=True,
        text=True,
    )


def main():

    with tempfile.TemporaryDirectory() as temp_dir:

        state_file = (
            Path(temp_dir)
            / "provider_health.json"
        )

        env = os.environ.copy()

        env[
            "PROVIDER_HEALTH_FILE"
        ] = str(state_file)

        result = run(
            """
from services.provider_health import provider_health

provider_health.clear()

provider_health.record_failure(
    "openrouter",
    RuntimeError(
        "503 Service Unavailable"
    ),
    cooldown=30,
)

assert (
    provider_health.available(
        "openrouter",
    )
    is False
)

print("WRITE_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "WRITE_OK"
            in result.stdout
        )

        assert state_file.exists()

        result = run(
            """
from services.provider_health import provider_health

assert (
    provider_health.available(
        "openrouter",
    )
    is False
)

assert (
    provider_health.status(
        "openrouter",
    )
    == "cooldown"
)

assert (
    provider_health.get(
        "openrouter",
    ).failures
    == 1
)

provider_health.record_success(
    "openrouter",
)

assert (
    provider_health.available(
        "openrouter",
    )
    is True
)

assert (
    provider_health.status(
        "openrouter",
    )
    == "healthy"
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

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ljcli.main",
                "health",
            ],
            env=env,
            capture_output=True,
            text=True,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        output = result.stdout

        assert (
            "LUMINOUS JOURNEY STUDIO"
            in output
        )

        assert (
            "PROVIDER HEALTH"
            in output
        )

    print(
        "PASS : provider health persists across processes"
    )

    print(
        "PASS : provider cooldown survives restart"
    )

    print(
        "PASS : provider recovery clears health state"
    )

    print(
        "PASS : health CLI remains operational"
    )

    print()

    print("=" * 60)

    print(
        "FINAL RELIABILITY TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()