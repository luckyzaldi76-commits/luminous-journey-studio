from services.ai_service import AIService
from services.provider_health import provider_health


def main():

    provider_health.clear()

    first = AIService(
        "openrouter",
    )

    provider_health.record_failure(
        "openrouter",
        RuntimeError(
            "402 insufficient credits"
        ),
    )

    assert (
        provider_health.available(
            "openrouter",
        )
        is False
    )

    second = AIService(
        "openrouter",
    )

    assert first is not second

    assert (
        second.provider_name
        == "openrouter"
    )

    assert (
        provider_health.available(
            "openrouter",
        )
        is False
    )

    health = provider_health.get(
        "openrouter",
    )

    assert health.failures == 1

    assert (
        health.last_error
        == "402 insufficient credits"
    )

    provider_health.record_success(
        "openrouter",
    )

    third = AIService(
        "openrouter",
    )

    assert (
        provider_health.available(
            "openrouter",
        )
        is True
    )

    assert (
        provider_health.get(
            "openrouter",
        ).failures
        == 0
    )

    provider_health.clear()

    print(
        "PASS : health survives AIService recreation"
    )

    print(
        "PASS : failed provider remains unavailable"
    )

    print(
        "PASS : health state is shared across services"
    )

    print(
        "PASS : success clears persistent health state"
    )

    print()

    print("=" * 60)

    print(
        "PROVIDER HEALTH PERSISTENCE TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()