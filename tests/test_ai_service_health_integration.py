from services.ai_service import AIService
from services.provider_health import provider_health


def main():

    provider_health.clear()

    service = AIService(
        "openrouter",
    )

    assert (
        service.name
        == "openrouter"
    )

    provider_health.record_failure(
        "openrouter",
        RuntimeError(
            "503 Service Unavailable"
        ),
        cooldown=30,
    )

    assert (
        provider_health.available(
            "openrouter",
        )
        is False
    )

    available = (
        service._available_provider_names()
    )

    assert (
        "openrouter"
        not in available
    )

    assert (
        "gemini"
        in available
    )

    assert (
        "mock"
        in available
    )

    provider_health.record_success(
        "openrouter",
    )

    available = (
        service._available_provider_names()
    )

    assert (
        "openrouter"
        in available
    )

    provider_health.clear()

    print(
        "PASS : AIService reads provider health"
    )

    print(
        "PASS : cooled provider is excluded from routing"
    )

    print(
        "PASS : healthy fallback providers remain available"
    )

    print(
        "PASS : recovered provider returns to routing"
    )

    print()

    print("=" * 60)

    print(
        "AI SERVICE HEALTH INTEGRATION TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()