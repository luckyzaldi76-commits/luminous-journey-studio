from services.provider_health import ProviderHealth


def main():

    health = ProviderHealth()

    health.record_failure(
        RuntimeError(
            "500 Internal Server Error"
        ),
        cooldown=1,
    )

    assert health.is_available() is False

    health.disabled_until = 0.0

    assert health.is_available() is True

    health.record_failure(
        RuntimeError(
            "429 RESOURCE_EXHAUSTED"
        ),
        cooldown=1,
    )

    assert health.is_available() is False

    health.disabled_until = 0.0

    assert health.is_available() is True

    health.record_failure(
        RuntimeError(
            "temporary provider failure"
        ),
        cooldown=1,
    )

    assert health.is_available() is False

    health.disabled_until = 0.0

    assert health.is_available() is True

    print(
        "PASS : expired server cooldown becomes available"
    )

    print(
        "PASS : expired quota cooldown becomes available"
    )

    print(
        "PASS : expired default cooldown becomes available"
    )

    print()

    print("=" * 60)

    print(
        "PROVIDER HEALTH EXPIRY TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()