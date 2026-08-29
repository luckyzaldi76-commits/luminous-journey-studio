import os
import subprocess
import sys
import tempfile
from pathlib import Path


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

        writer = subprocess.run(
            [
                sys.executable,
                "-c",
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
""",
            ],
            env=env,
            capture_output=True,
            text=True,
        )

        assert (
            writer.returncode == 0
        ), writer.stderr

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

        assert (
            "Provider       : openrouter"
            in output
        )

        assert (
            "Status         : cooldown"
            in output
        )

        assert (
            "Failures       : 1"
            in output
        )

        assert (
            "Available      : False"
            in output
        )

        assert (
            "Remaining"
            in output
        )

    print(
        "PASS : CLI health command executes"
    )

    print(
        "PASS : CLI exposes provider status"
    )

    print(
        "PASS : CLI exposes provider failures"
    )

    print(
        "PASS : CLI exposes cooldown information"
    )

    print()

    print("=" * 60)

    print(
        "CLI HEALTH TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()