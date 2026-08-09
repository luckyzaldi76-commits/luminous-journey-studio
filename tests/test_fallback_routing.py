import os

from services.fallback_service import FallbackService


def main():

    original_provider = os.environ.get(
        "AI_PROVIDER"
    )

    original_mock = os.environ.get(
        "USE_MOCK"
    )

    try:

        # ==================================================
        # USE_MOCK=True MUST FORCE MOCK
        # ==================================================

        os.environ["AI_PROVIDER"] = "auto"
        os.environ["USE_MOCK"] = "True"

        service = FallbackService()

        assert (
            service.provider == "mock"
        ), (
            "USE_MOCK=True must force "
            "MockProvider."
        )

        print(
            "PASS : USE_MOCK=True -> mock"
        )

        # ==================================================
        # EXPLICIT MOCK
        # ==================================================

        os.environ["AI_PROVIDER"] = "mock"
        os.environ["USE_MOCK"] = "False"

        service = FallbackService()

        assert (
            service.provider == "mock"
        ), (
            "AI_PROVIDER=mock must select "
            "MockProvider."
        )

        print(
            "PASS : AI_PROVIDER=mock -> mock"
        )

        # ==================================================
        # AUTO WITHOUT MOCK
        # ==================================================

        os.environ["AI_PROVIDER"] = "auto"
        os.environ["USE_MOCK"] = "False"

        service = FallbackService()

        assert (
            service.provider == "openrouter"
        ), (
            "AI_PROVIDER=auto with "
            "USE_MOCK=False must select "
            "OpenRouter."
        )

        print(
            "PASS : auto + mock=False -> openrouter"
        )

        print()
        print("=" * 60)
        print("FALLBACK ROUTING TEST PASSED")
        print("=" * 60)

    finally:

        if original_provider is None:

            os.environ.pop(
                "AI_PROVIDER",
                None,
            )

        else:

            os.environ[
                "AI_PROVIDER"
            ] = original_provider

        if original_mock is None:

            os.environ.pop(
                "USE_MOCK",
                None,
            )

        else:

            os.environ[
                "USE_MOCK"
            ] = original_mock


if __name__ == "__main__":
    main()