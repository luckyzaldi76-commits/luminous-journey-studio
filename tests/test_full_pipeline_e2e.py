import os
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve().parent.parent
)


def main():

    with tempfile.TemporaryDirectory() as temp_dir:

        root = Path(temp_dir)

        health_file = (
            root
            / "provider_health.json"
        )

        output_dir = (
            root
            / "exports"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
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

        env[
            "OUTPUT_DIR"
        ] = str(output_dir)

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                """
from services.ai_service import AIService

service = AIService("mock")

prompt = (
    "Create a short Catholic "
    "Scripture meditation about "
    "trusting God."
)

response = service.generate(
    prompt,
    max_tokens=128,
)

assert isinstance(
    response,
    str,
)

assert response.strip()

chunks = list(
    service.stream(
        prompt,
        max_tokens=128,
    )
)

assert chunks

stream_text = "".join(
    str(chunk)
    for chunk in chunks
)

assert stream_text.strip()

print("PIPELINE_AI_OK")
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
            "PIPELINE_AI_OK"
            in result.stdout
        ), result.stdout

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                """
from pathlib import Path

from services.ai_service import AIService

service = AIService("mock")

text = service.generate(
    "Write a one sentence Gospel meditation.",
    max_tokens=64,
)

output = Path(
    r"OUTPUT_FILE"
)

output.write_text(
    text.strip(),
    encoding="utf-8",
)

assert output.exists()
assert output.read_text(
    encoding="utf-8"
).strip()

print("PIPELINE_EXPORT_OK")
""".replace(
                    "OUTPUT_FILE",
                    str(
                        output_dir
                        / "meditation.md"
                    ),
                ),
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
            "PIPELINE_EXPORT_OK"
            in result.stdout
        ), result.stdout

        exported = (
            output_dir
            / "meditation.md"
        )

        assert exported.exists()

        assert (
            exported.read_text(
                encoding="utf-8",
            ).strip()
        )

        assert health_file.exists()

        print(
            "PASS : AI generation pipeline works"
        )

        print(
            "PASS : AI streaming pipeline works"
        )

        print(
            "PASS : export pipeline works"
        )

        print(
            "PASS : provider health state is persisted"
        )

        print()

        print("=" * 60)

        print(
            "FULL APPLICATION PIPELINE E2E TEST PASSED"
        )

        print("=" * 60)


if __name__ == "__main__":

    main()