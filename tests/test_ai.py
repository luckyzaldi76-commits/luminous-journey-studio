from services.fallback_service import FallbackService


def main():

    ai = FallbackService()

    prompt = """
Say hello in one short sentence.
"""

    print("=" * 60)
    print("AI TEST")
    print("=" * 60)
    print()

    response = ai.generate(prompt)

    print(response)

    print()
    print("=" * 60)
    print("AI TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":

    main()