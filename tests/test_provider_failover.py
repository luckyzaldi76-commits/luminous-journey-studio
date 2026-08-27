from services.ai_service import AIService


def main():

    service = AIService("openrouter")

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

            raise RuntimeError(
                "OpenRouter simulated failure"
            )

        if provider_name == "gemini":

            raise RuntimeError(
                "Gemini simulated failure"
            )

        if provider_name == "mock":

            return (
                "# TITLE\n\n"
                "Failover Test\n\n"
                "# SCRIPT\n\n"
                "Mock fallback succeeded."
            )

        raise RuntimeError(
            f"Unexpected provider: {provider_name}"
        )

    service._generate_with_provider = fake_generate

    result = service.generate(
        "Failover test",
        max_tokens=100,
    )

    assert result

    assert calls == [
        "openrouter",
        "gemini",
        "mock",
    ], calls

    assert service.name == "mock"

    assert "Failover Test" in result

    print(
        "PASS : openrouter -> gemini -> mock"
    )

    print(
        "PASS : failed providers skipped"
    )

    print(
        "PASS : successful provider becomes active"
    )

    print()

    print("=" * 60)

    print(
        "PROVIDER FAILOVER TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()