from services.fallback_service import FallbackService


def main():

    ai = FallbackService()

    result = ai.generate(

        "Say hello in one sentence."

    )

    assert result

    assert "# TITLE" in result

    assert "# SCRIPT" in result

    print()

    print("=" * 60)

    print("FALLBACK SERVICE TEST PASSED")

    print("=" * 60)

    print()

    print(result)


if __name__ == "__main__":

    main()