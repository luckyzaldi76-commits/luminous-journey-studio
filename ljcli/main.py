import argparse
from pathlib import Path

from engine.production_engine import ProductionEngine


def main():

    parser = argparse.ArgumentParser(
        prog="luminous",
    )

    parser.add_argument(
        "workflow",
    )

    parser.add_argument(
        "--gospel",
        required=True,
    )

    parser.add_argument(
        "--language",
        default="English",
    )

    parser.add_argument(
        "--audience",
        default="Adults",
    )

    parser.add_argument(
        "--output",
        default="exports",
    )

    args = parser.parse_args()

    ProductionEngine().run(
        workflow_name=args.workflow,
        gospel=args.gospel,
        language=args.language,
        audience=args.audience,
        output_dir=Path(args.output),
    )


if __name__ == "__main__":
    main()