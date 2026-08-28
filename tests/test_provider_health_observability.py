from services.provider_health import ProviderHealthRegistry


def main():

    registry = ProviderHealthRegistry()

    registry.clear()

    assert (
        registry.status(
            "openrouter",
        )
        == "healthy"
    )

    registry.record_failure(
        "openrouter",
        RuntimeError(
            "503 Service Unavailable"
        ),
        cooldown=30,
    )

    assert (
        registry.status(
            "openrouter",
        )
        == "cooldown"
    )

    assert (
        registry.available(
            "openrouter",
        )
        is False
    )

    snapshot = registry.snapshot()

    assert (
        "openrouter"
        in snapshot
    )

    assert (
        snapshot["openrouter"]["status"]
        == "cooldown"
    )

    assert (
        snapshot["openrouter"]["failures"]
        == 1
    )

    assert (
        snapshot["openrouter"]["available"]
        is False
    )

    assert (
        snapshot["openrouter"]["remaining_cooldown"]
        > 0
    )

    registry.record_success(
        "openrouter",
    )

    assert (
        registry.status(
            "openrouter",
        )
        == "healthy"
    )

    snapshot = registry.snapshot()

    assert (
        snapshot["openrouter"]["failures"]
        == 0
    )

    assert (
        snapshot["openrouter"]["last_error"]
        == ""
    )

    assert (
        snapshot["openrouter"]["available"]
        is True
    )

    assert (
        snapshot["openrouter"]["remaining_cooldown"]
        == 0
    )

    registry.clear()

    print(
        "PASS : healthy provider exposes healthy status"
    )

    print(
        "PASS : failed provider exposes cooldown status"
    )

    print(
        "PASS : snapshot exposes safe health metrics"
    )

    print(
        "PASS : successful provider returns to healthy status"
    )

    print()

    print("=" * 60)

    print(
        "PROVIDER HEALTH OBSERVABILITY TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()