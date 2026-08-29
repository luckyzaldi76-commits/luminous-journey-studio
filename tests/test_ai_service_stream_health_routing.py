from services.ai_service import AIService
from services.provider_health import provider_health


def main():

    provider_health.clear()

    service = AIService(
        "openrouter",
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

    chunks = list(
        service.stream(
            "Return exactly: STREAM HEALTH ROUTING OK",
            max_tokens=32,
        )
    )

    assert chunks

    assert (
        service.name
        != "openrouter"
    )

    assert (
        service.name
        in {
            "gemini",
            "mock",
        }
    )

    assert (
        provider_health.available(
            service.name,
        )
        is True
    )

    provider_health.clear()

    print(
        "PASS : stream skips cooled provider"
    )

    print(
        "PASS : stream selects healthy fallback"
    )

    print(
        "PASS : selected stream provider is healthy"
    )

    print()

    print("=" * 60)

    print(
        "AI SERVICE STREAM HEALTH ROUTING TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()