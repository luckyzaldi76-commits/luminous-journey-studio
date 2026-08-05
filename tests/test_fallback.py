from services.fallback_service import FallbackService


def main():

    ai = FallbackService()

    result = ai.generate(
        "Say hello in one sentence."
    )

    print(result)


if __name__ == "__main__":
    main()