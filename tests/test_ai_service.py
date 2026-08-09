from services.ai_service import AIService


def main():

    ai = AIService(

        "mock",

    )

    response = ai.generate(

        "Say Hello",

    )

    assert response

    assert "# TITLE" in response

    assert "# SCRIPT" in response

    print()

    print("=" * 60)

    print("AI SERVICE TEST PASSED")

    print("=" * 60)

    print()

    print(response)


if __name__ == "__main__":

    main()