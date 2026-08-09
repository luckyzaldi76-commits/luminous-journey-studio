import argparse
from pathlib import Path

from config.settings import OUTPUT_DIR
from engine.production_engine import ProductionEngine
from luminous.kernel.registry import WorkflowRegistry
from luminous.workflows.dailygospelworkflow import (
    DailyGospelWorkflow,
)


WorkflowRegistry.register(

    "daily_gospel",

    DailyGospelWorkflow,

)


def main():

    parser = argparse.ArgumentParser(

        prog="luminous",

        description="Luminous Journey Studio CLI",

    )

    parser.add_argument(

        "workflow",

        choices=WorkflowRegistry.names(),

        help="Workflow name",

    )

    parser.add_argument(

        "--gospel",

        required=True,

        help="Gospel passage",

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

        default=str(OUTPUT_DIR),

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