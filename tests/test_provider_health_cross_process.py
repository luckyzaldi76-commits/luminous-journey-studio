import json
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
        "402 insufficient credits"
    ),
)

print(
    provider_health.available(
        "openrouter",
    )
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

        assert (
            "False"
            in writer.stdout
        ), writer.stdout

        assert state_file.exists()

        data = json.loads(
            state_file.read_text(
                encoding="utf-8",
            )
        )

        assert (
            "providers"
            in data
        )

        assert (
            "openrouter"
            in data["providers"]
        )

        reader = subprocess.run(

            [
                sys.executable,
                "-c",
                """
from services.provider_health import provider_health

print(
    provider_health.available(
        "openrouter",
    )
)

print(
    provider_health.get(
        "openrouter",
    ).failures
)
""",
            ],

            env=env,

            capture_output=True,

            text=True,

        )

        assert (
            reader.returncode == 0
        ), reader.stderr

        lines = [
            line.strip()
            for line in reader.stdout.splitlines()
            if line.strip()
        ]

        assert (
            "False"
            in lines
        ), reader.stdout

        assert (
            "1"
            in lines
        ), reader.stdout

    print(
        "PASS : process A persists provider health"
    )

    print(
        "PASS : process B restores provider health"
    )

    print(
        "PASS : cooldown remains active across processes"
    )

    print()

    print("=" * 60)

    print(
        "CROSS-PROCESS PROVIDER HEALTH TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()