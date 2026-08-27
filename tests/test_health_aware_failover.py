from services.ai_service import AIService
from services.provider_health import provider_health


def main():

    provider_health.clear()

    service = AIService(
        "openrouter",
    )

    calls = []

    def fake_generate(
        provider_name,
        prompt,
        max_tokens,
    ):

        calls.append(
            provider_name,
        )

        if provider_name == "openrouter":

            error = RuntimeError(
                "402 insufficient credits"
            )

            provider_health.record_failure(
                provider_name,
                error,
            )

            raise error

        if provider_name == "gemini":

            provider_health.record_success(
                provider_name,
            )

            return (
                "# TITLE\n\n"
                "Gemini Success\n\n"
                "# SCRIPT\n\n"
                "Gemini fallback succeeded."
            )

        if provider_name == "mock":

            provider_health.record_success(
                provider_name,
            )

            return (
                "# TITLE\n\n"
                "Mock Success\n\n"
                "# SCRIPT\n\n"
                "Mock fallback succeeded."
            )

        raise RuntimeError(
            f"Unexpected provider: {provider_name}"
        )

    service._generate_with_provider = (
        fake_generate
    )

    first = service.generate(
        "Health aware failover test",
        max_tokens=100,
    )

    assert (
        "Gemini Success"
        in first
    )

    assert calls == [
        "openrouter",
        "gemini",
    ], calls

    assert service.name == "gemini"

    assert (
        provider_health.available(
            "openrouter",
        )
        is False
    )

    calls.clear()

    second = service.generate(
        "Second request",
        max_tokens=100,
    )

    assert (
        "Gemini Success"
        in second
    )

    assert calls == [
        "gemini",
    ], calls

    assert service.name == "gemini"

    provider_health.clear()

    print(
        "PASS : failed provider enters cooldown"
    )

    print(
        "PASS : healthy fallback provider is used"
    )

    print(
        "PASS : cooled-down provider is skipped"
    )

    print(
        "PASS : subsequent request uses healthy provider"
    )

    print()

    print("=" * 60)

    print(
        "HEALTH-AWARE FAILOVER TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()