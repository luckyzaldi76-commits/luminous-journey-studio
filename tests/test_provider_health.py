from services.provider_health import (
    ProviderHealth,
    ProviderHealthRegistry,
)


def main():

    health = ProviderHealth()

    assert health.failures == 0
    assert health.last_error == ""
    assert health.is_available() is True

    health.record_failure(
        RuntimeError(
            "429 RESOURCE_EXHAUSTED"
        ),
        cooldown=60,
    )

    assert health.failures == 1
    assert (
        health.last_error
        == "429 RESOURCE_EXHAUSTED"
    )
    assert health.is_available() is False

    health.record_success()

    assert health.failures == 0
    assert health.last_error == ""
    assert health.is_available() is True

    registry = ProviderHealthRegistry()

    assert registry.available(
        "openrouter"
    ) is True

    registry.record_failure(
        "openrouter",
        RuntimeError(
            "402 insufficient credits"
        ),
        cooldown=60,
    )

    assert registry.available(
        "openrouter"
    ) is False

    snapshot = registry.snapshot()

    assert (
        snapshot["openrouter"]["failures"]
        == 1
    )

    assert (
        snapshot["openrouter"]["last_error"]
        == "402 insufficient credits"
    )

    assert (
        snapshot["openrouter"]["available"]
        is False
    )

    registry.record_success(
        "openrouter",
    )

    assert registry.available(
        "openrouter"
    ) is True

    assert (
        registry.snapshot()[
            "openrouter"
        ]["failures"]
        == 0
    )

    registry.record_failure(
        "gemini",
        RuntimeError(
            "429 quota exceeded"
        ),
        cooldown=60,
    )

    assert registry.available(
        "gemini"
    ) is False

    assert registry.available(
        "mock"
    ) is True

    registry.reset(
        "gemini",
    )

    assert registry.available(
        "gemini"
    ) is True

    registry.clear()

    assert registry.snapshot() == {}

    print(
        "PASS : provider health starts available"
    )

    print(
        "PASS : failure disables provider"
    )

    print(
        "PASS : success resets provider health"
    )

    print(
        "PASS : registry tracks providers independently"
    )

    print(
        "PASS : reset and clear work correctly"
    )

    print()

    print("=" * 60)

    print(
        "PROVIDER HEALTH TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()