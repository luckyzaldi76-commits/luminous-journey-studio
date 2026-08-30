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

        root = Path(temp_dir)

        health_file = (
            root
            / "provider_health.json"
        )

        env = os.environ.copy()

        env["AI_PROVIDER"] = "mock"
        env["USE_MOCK"] = "true"
        env["DEBUG"] = "false"
        env["PROVIDER_HEALTH_FILE"] = str(
            health_file
        )

        result = run(
            """
from config import settings

assert settings.APP_NAME
assert settings.VERSION
assert settings.LANGUAGES
assert settings.AI_PROVIDER == "mock"
assert settings.USE_MOCK is True

print("CONFIG_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "CONFIG_OK"
            in result.stdout
        ), result.stdout

        result = run(
            """
from services.ai_service import AIService

service = AIService("mock")

assert service.name == "mock"

text = service.generate(
    "Write a short sentence about hope.",
    max_tokens=64,
)

assert isinstance(text, str)
assert text.strip()

print("GENERATE_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "GENERATE_OK"
            in result.stdout
        ), result.stdout

        result = run(
            """
from services.ai_service import AIService

service = AIService("mock")

chunks = list(
    service.stream(
        "Say hello briefly.",
        max_tokens=64,
    )
)

assert chunks

text = "".join(
    str(chunk)
    for chunk in chunks
)

assert text.strip()

print("STREAM_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "STREAM_OK"
            in result.stdout
        ), result.stdout

        result = run(
            """
from services.provider_health import (
    ProviderHealthRegistry,
)

registry = ProviderHealthRegistry()

registry.clear()

registry.record_failure(
    "mock",
    RuntimeError("temporary failure"),
    cooldown=1,
)

assert not registry.available("mock")

registry.record_success("mock")

assert registry.available("mock")

assert (
    registry.status("mock")
    == "healthy"
)

print("HEALTH_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "HEALTH_OK"
            in result.stdout
        ), result.stdout

        result = run(
            """
from services.ai_service import AIService

service = AIService("mock")

for index in range(3):

    response = service.generate(
        f"Generate test message {index}.",
        max_tokens=32,
    )

    assert response.strip()

print("REPEATED_GENERATION_OK")
""",
            env,
        )

        assert (
            result.returncode == 0
        ), result.stderr

        assert (
            "REPEATED_GENERATION_OK"
            in result.stdout
        ), result.stdout

        assert health_file.exists()

    print(
        "PASS : configuration validation"
    )

    print(
        "PASS : AI generation"
    )

    print(
        "PASS : AI streaming"
    )

    print(
        "PASS : provider health recovery"
    )

    print(
        "PASS : repeated generation stability"
    )

    print(
        "PASS : provider health persistence"
    )

    print()

    print("=" * 60)

    print(
        "FULL SYSTEM VALIDATION TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()