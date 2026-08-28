from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

from services.provider_health import ProviderHealthRegistry


def main():

    with TemporaryDirectory() as temp_dir:

        state_file = (
            Path(temp_dir)
            / "provider_health.json"
        )

        registry = ProviderHealthRegistry(
            state_file=state_file,
        )

        registry.clear()

        errors = [
            RuntimeError(
                f"503 failure {index}"
            )
            for index in range(20)
        ]

        def record(
            error,
        ):

            registry.record_failure(
                "openrouter",
                error,
                cooldown=30,
            )

        with ThreadPoolExecutor(
            max_workers=10,
        ) as executor:

            list(
                executor.map(
                    record,
                    errors,
                )
            )

        health = registry.get(
            "openrouter",
        )

        assert health.failures == 20

        assert (
            health.last_error.startswith(
                "503 failure"
            )
        )

        assert (
            registry.available(
                "openrouter",
            )
            is False
        )

        assert state_file.exists()

        restored = ProviderHealthRegistry(
            state_file=state_file,
        )

        restored_health = restored.get(
            "openrouter",
        )

        assert (
            restored_health.failures
            == 20
        )

        assert (
            restored.available(
                "openrouter",
            )
            is False
        )

    print(
        "PASS : concurrent failures are counted"
    )

    print(
        "PASS : concurrent state remains unavailable"
    )

    print(
        "PASS : persisted state remains valid"
    )

    print(
        "PASS : concurrent state restores correctly"
    )

    print()

    print("=" * 60)

    print(
        "PROVIDER HEALTH CONCURRENCY TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()