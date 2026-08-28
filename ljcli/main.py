import argparse

from config.settings import (
    AI_PROVIDER,
    GEMINI_MODEL,
    OPENROUTER_MODEL,
    USE_MOCK,
    VERSION,
)
from services.provider_health import provider_health


def _print_header():

    print("=" * 60)
    print("LUMINOUS JOURNEY STUDIO")
    print("=" * 60)

    print(
        f"Version        : {VERSION}"
    )

    print(
        f"AI Provider    : {AI_PROVIDER}"
    )

    print(
        f"Mock           : {USE_MOCK}"
    )

    print(
        f"Gemini Model   : {GEMINI_MODEL}"
    )

    print(
        f"OpenRouter     : {OPENROUTER_MODEL}"
    )

    print("=" * 60)


def _print_health():

    snapshot = provider_health.snapshot()

    print()
    print("=" * 60)
    print("PROVIDER HEALTH")
    print("=" * 60)

    if not snapshot:

        print(
            "No provider health state."
        )

        print("=" * 60)

        return

    for name, health in snapshot.items():

        print(
            f"Provider       : {name}"
        )

        print(
            f"Status         : {health['status']}"
        )

        print(
            f"Failures       : {health['failures']}"
        )

        print(
            f"Available      : {health['available']}"
        )

        print(
            "Remaining      : "
            f"{health['remaining_cooldown']:.1f}s"
        )

        if health["last_error"]:

            print(
                f"Last Error     : "
                f"{health['last_error']}"
            )

        print("-" * 60)

    print("=" * 60)


def build_parser():

    parser = argparse.ArgumentParser(
        prog="ljcli",
        description=(
            "Luminous Journey Studio CLI"
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
    )

    subparsers.add_parser(
        "health",
        help="Show provider health",
    )

    return parser


def main(
    argv=None,
):

    parser = build_parser()

    args = parser.parse_args(
        argv,
    )

    _print_header()

    if args.command == "health":

        _print_health()

        return 0

    return 0


if __name__ == "__main__":

    raise SystemExit(
        main()
    )