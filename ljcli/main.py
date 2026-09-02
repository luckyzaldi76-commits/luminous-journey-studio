import argparse
from pathlib import Path

from config.settings import (
    AI_PROVIDER,
    GEMINI_MODEL,
    OPENROUTER_MODEL,
    USE_MOCK,
    VERSION,
)

from services.production_orchestrator import (
    ProductionOrchestrator,
)
from services.provider_health import (
    provider_health,
)
from services.workflow_registry import (
    workflow_registry,
)


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

        return 0

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

    return 0


def _print_workflows():

    print()
    print("=" * 60)
    print("AVAILABLE WORKFLOWS")
    print("=" * 60)

    for name in workflow_registry.names():

        print(name)

    print("=" * 60)

    return 0


def _print_result(
    result,
    title,
):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    if "gospel" in result:

        print(
            f"Gospel         : {result['gospel']}"
        )

    if "languages" in result:

        print(
            f"Languages      : "
            f"{', '.join(result['languages'])}"
        )

    if "audience" in result:

        print(
            f"Audience       : {result['audience']}"
        )

    if "workflow" in result:

        print(
            f"Workflow       : {result['workflow']}"
        )

    if "total_jobs" in result:

        print(
            f"Total Jobs     : "
            f"{result['total_jobs']}"
        )

    if "recovered_jobs" in result:

        print(
            f"Recovered      : "
            f"{result['recovered_jobs']}"
        )

    if "completed_jobs" in result:

        print(
            f"Completed      : "
            f"{result['completed_jobs']}"
        )

    if "failed_jobs" in result:

        print(
            f"Failed         : "
            f"{result['failed_jobs']}"
        )

    progress = result.get(
        "progress"
    )

    if progress:

        print(
            f"Progress       : "
            f"{progress['percentage']:.2f}%"
        )

        print(
            f"State          : "
            f"{progress['state']}"
        )

    if "output_dir" in result:

        print(
            f"Output         : "
            f"{result['output_dir']}"
        )

    print(
        f"Success        : "
        f"{result['success']}"
    )

    print("=" * 60)


def _create_orchestrator():

    return ProductionOrchestrator()


def _generate(args):

    output_dir = Path(
        args.output_dir
    )

    orchestrator = _create_orchestrator()

    result = orchestrator.run(
        gospel=args.gospel,
        languages=(args.language,),
        audience=args.audience,
        output_dir=output_dir,
        workflow_name=args.workflow,
    )

    _print_result(
        result,
        "PRODUCTION GENERATION COMPLETE",
    )

    return 0 if result["success"] else 1


def _batch(args):

    languages = tuple(
        language.strip().upper()
        for language in args.languages.split(",")
        if language.strip()
    )

    if not languages:

        raise ValueError(
            "At least one language is required."
        )

    output_dir = Path(
        args.output_dir
    )

    orchestrator = _create_orchestrator()

    result = orchestrator.run(
        gospel=args.gospel,
        languages=languages,
        audience=args.audience,
        output_dir=output_dir,
        workflow_name=args.workflow,
    )

    _print_result(
        result,
        "PRODUCTION BATCH COMPLETE",
    )

    return 0 if result["success"] else 1


def _recover(args):

    orchestrator = _create_orchestrator()

    result = orchestrator.recover()

    _print_result(
        result,
        "PRODUCTION RECOVERY COMPLETE",
    )

    return 0 if result["success"] else 1


def build_parser():

    parser = argparse.ArgumentParser(
        prog="ljcli",
        description=(
            "Luminous Journey Studio"
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
    )

    subparsers.add_parser(
        "health",
        help="Show provider health",
    )

    subparsers.add_parser(
        "workflows",
        help="List available workflows",
    )

    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate production content",
    )

    generate_parser.add_argument(
        "--gospel",
        required=True,
        help="Gospel passage",
    )

    generate_parser.add_argument(
        "--language",
        required=True,
        help="Language code",
    )

    generate_parser.add_argument(
        "--audience",
        required=True,
        help="Target audience",
    )

    generate_parser.add_argument(
        "--output-dir",
        required=True,
        help="Production output directory",
    )

    generate_parser.add_argument(
        "--workflow",
        default="Daily Gospel",
        help="Workflow name",
    )

    batch_parser = subparsers.add_parser(
        "batch",
        help="Generate multilingual production batch",
    )

    batch_parser.add_argument(
        "--gospel",
        required=True,
        help="Gospel passage",
    )

    batch_parser.add_argument(
        "--languages",
        required=True,
        help=(
            "Comma-separated language codes"
        ),
    )

    batch_parser.add_argument(
        "--audience",
        required=True,
        help="Target audience",
    )

    batch_parser.add_argument(
        "--output-dir",
        required=True,
        help="Production output directory",
    )

    batch_parser.add_argument(
        "--workflow",
        default="Daily Gospel",
        help="Workflow name",
    )

    subparsers.add_parser(
        "recover",
        help="Recover interrupted production jobs",
    )

    return parser


def main(argv=None):

    parser = build_parser()

    args = parser.parse_args(
        argv
    )

    _print_header()

    if args.command == "health":

        return _print_health()

    if args.command == "workflows":

        return _print_workflows()

    if args.command == "generate":

        return _generate(args)

    if args.command == "batch":

        return _batch(args)

    if args.command == "recover":

        return _recover(args)

    return 0


if __name__ == "__main__":

    raise SystemExit(
        main()
    )