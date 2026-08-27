from services.provider_health import ProviderHealth


def main():

    health = ProviderHealth()

    health.record_failure(
        RuntimeError(
            "402 insufficient credits"
        )
    )

    quota_cooldown = (
        health.disabled_until
        - __import__(
            "services.provider_health",
            fromlist=["monotonic"],
        ).monotonic()
    )

    assert 295 <= quota_cooldown <= 300

    health.reset()

    health.record_failure(
        RuntimeError(
            "429 RESOURCE_EXHAUSTED"
        )
    )

    quota_cooldown = (
        health.disabled_until
        - __import__(
            "services.provider_health",
            fromlist=["monotonic"],
        ).monotonic()
    )

    assert 295 <= quota_cooldown <= 300

    health.reset()

    health.record_failure(
        RuntimeError(
            "500 Internal Server Error"
        )
    )

    server_cooldown = (
        health.disabled_until
        - __import__(
            "services.provider_health",
            fromlist=["monotonic"],
        ).monotonic()
    )

    assert 25 <= server_cooldown <= 30

    health.reset()

    health.record_failure(
        RuntimeError(
            "503 Service Unavailable"
        )
    )

    server_cooldown = (
        health.disabled_until
        - __import__(
            "services.provider_health",
            fromlist=["monotonic"],
        ).monotonic()
    )

    assert 25 <= server_cooldown <= 30

    health.reset()

    health.record_failure(
        RuntimeError(
            "unexpected provider failure"
        )
    )

    default_cooldown = (
        health.disabled_until
        - __import__(
            "services.provider_health",
            fromlist=["monotonic"],
        ).monotonic()
    )

    assert 55 <= default_cooldown <= 60

    print(
        "PASS : 402/429 -> 300 second cooldown"
    )

    print(
        "PASS : 500/503 -> 30 second cooldown"
    )

    print(
        "PASS : unknown error -> 60 second cooldown"
    )

    print()

    print("=" * 60)

    print(
        "PROVIDER COOLDOWN TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()