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


def main():

    with tempfile.TemporaryDirectory() as temp_dir:

        health_file = (
            Path(temp_dir)
            / "provider_health.json"
        )

        env = os.environ.copy()

        env[
            "AI_PROVIDER"
        ] = "mock"

        env[
            "USE_MOCK"
        ] = "true"

        env[
            "DEBUG"
        ] = "false"

        env[
            "PROVIDER_HEALTH_FILE"
        ] = str(health_file)

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                """
from services.ai_service import AIService
from services.provider_health import (
    ProviderHealthRegistry,
)

service = AIService("mock")

assert service.name == "mock"

response = service.generate(
    "Write one short sentence about hope.",
    max_tokens=32,
)

assert isinstance(
    response,
    str,
)

assert response.strip()

registry = ProviderHealthRegistry()

assert registry.available(
    "mock"
)

assert registry.status(
    "mock"
) in {
    "healthy",
    "available",
}

print("GENERATE_E2E_OK")
""",
            ],
            cwd=PROJECT_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "GENERATE_E2E_OK"
            in result.stdout
        ), result.stdout

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                """
from services.ai_service import AIService

service = AIService("mock")

chunks = list(
    service.stream(
        "Say hello in one short sentence.",
        max_tokens=32,
    )
)

assert chunks

text = "".join(
    str(chunk)
    for chunk in chunks
)

assert text.strip()

print("STREAM_E2E_OK")
""",
            ],
            cwd=PROJECT_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "STREAM_E2E_OK"
            in result.stdout
        ), result.stdout

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ljcli.main",
                "health",
            ],
            cwd=PROJECT_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "Status"
            in result.stdout
        ), result.stdout

        print(
            "PASS : AI generate flow works"
        )

        print(
            "PASS : AI streaming flow works"
        )

        print(
            "PASS : CLI health flow works"
        )

        print()

        print("=" * 60)

        print(
            "E2E PRODUCTION FLOW TEST PASSED"
        )

        print("=" * 60)


if __name__ == "__main__":

    main()