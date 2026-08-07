from pathlib import Path
import time

from luminous.context.pipeline_context import PipelineContext
from luminous.kernel.event_bus import EventBus
from luminous.kernel.runtime import Runtime
from luminous.kernel.scheduler import Scheduler

from luminous.workflows.dailygospelworkflow import (
    DailyGospelWorkflow,
)

from services.builder_service import BuilderService
from services.exporter_service import ExporterService


class ProductionEngine:

    def __init__(self):

        self.runtime = Runtime(

            scheduler=Scheduler(),

            event_bus=EventBus(),

        )

    def run(

        self,

        gospel: str,

        language: str,

        audience: str,

        output_dir: Path,

    ):

        start = time.perf_counter()

        print()
        print("=" * 60)
        print("LUMINOUS JOURNEY STUDIO")
        print("=" * 60)
        print()

        context = PipelineContext(

            gospel=gospel,

            language=language,

            audience=audience,

        )

        workflow = DailyGospelWorkflow()

        print("Running Workflow...")
        print()

        self.runtime.run(

            workflow,

            context,

        )

        print("✓ Workflow completed")
        print()

        data = BuilderService.build(
            context,
        )

        print("Exporting...")
        print()

        ExporterService.export(

            output_dir,

            data,

        )

        elapsed = time.perf_counter() - start

        print("Done.")
        print()

        print(
            f"Total Time : {elapsed:.2f} sec"
        )

        print()

        return data