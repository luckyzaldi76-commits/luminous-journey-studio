from providers.factory import ProviderFactory


def main():

    provider = ProviderFactory.create(
        "openrouter",
    )

    print()

    print("=" * 60)

    print("PROVIDER TEST PASSED")

    print("=" * 60)

    print()

    print(type(provider).__name__)

    print(provider)


if __name__ == "__main__":

    main()