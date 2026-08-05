from services.fallback_service import FallbackService


def main():

    ai = FallbackService()

    print("=" * 60)
    print("LUMINOUS JOURNEY STREAM TEST")
    print("=" * 60)
    print()

    for chunk in ai.stream(
        prompt="Write one paragraph about Jesus.",
        max_tokens=300,
    ):

        print(
            chunk,
            end="",
            flush=True,
        )

    print()
    print()
    print("=" * 60)
    print("STREAM FINISHED")
    print("=" * 60)


if __name__ == "__main__":
    main()