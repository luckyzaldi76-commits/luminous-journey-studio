from pathlib import Path

from config import settings


def main():

    assert (
        isinstance(
            settings.PROVIDER_HEALTH_FILE,
            Path,
        )
    )

    assert (
        settings.PROVIDER_HEALTH_DEFAULT_COOLDOWN
        > 0
    )

    assert (
        settings.PROVIDER_HEALTH_QUOTA_COOLDOWN
        >= settings.PROVIDER_HEALTH_DEFAULT_COOLDOWN
    )

    assert (
        settings.PROVIDER_HEALTH_SERVER_COOLDOWN
        > 0
    )

    assert (
        settings.PROVIDER_HEALTH_QUOTA_COOLDOWN
        > settings.PROVIDER_HEALTH_SERVER_COOLDOWN
    )

    assert (
        settings.REQUEST_TIMEOUT
        > 0
    )

    assert (
        settings.MAX_RETRY
        >= 0
    )

    assert (
        settings.AI_PROVIDER
        in {
            "auto",
            "mock",
            "gemini",
            "openrouter",
        }
    )

    assert (
        isinstance(
            settings.USE_MOCK,
            bool,
        )
    )

    assert (
        settings.OPENROUTER_MAX_TOKENS
        == settings.STAGE1_MAX_TOKENS
    )

    assert (
        len(settings.LANGUAGES)
        >= 1
    )

    print(
        "PASS : provider health configuration is valid"
    )

    print(
        "PASS : cooldown configuration is consistent"
    )

    print(
        "PASS : request configuration is valid"
    )

    print(
        "PASS : AI provider configuration is valid"
    )

    print(
        "PASS : token configuration is consistent"
    )

    print()

    print("=" * 60)

    print(
        "PRODUCTION CONFIG TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()