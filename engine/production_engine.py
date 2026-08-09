from pathlib import Path

from luminous.context.pipeline_context import PipelineContext
from luminous.kernel.event_bus import EventBus
from luminous.kernel.runtime import Runtime
from luminous.kernel.scheduler import Scheduler
from luminous.workflows.dailygospelworkflow import DailyGospelWorkflow

from services.builder_service import BuilderService
from luminous.infrastructure.exporters.exporter_service import ExporterService


class ProductionEngine:

    def __init__(self):

        self.builder = BuilderService()
        self.exporter = ExporterService()

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
        workflow_name: str = "Daily Gospel",
    ) -> dict:

        context = PipelineContext(
            gospel=gospel,
            language=language,
            audience=audience,
        )

        workflow = DailyGospelWorkflow()

        self.runtime.run(
            workflow,
            context,
        )

        data = self.builder.build(
            context,
        )

        data.setdefault(
            "gospel",
            gospel,
        )

        data.setdefault(
            "language",
            language,
        )

        data.setdefault(
            "audience",
            audience,
        )

        self.exporter.export(
            output_dir,
            data,
        )

        return data