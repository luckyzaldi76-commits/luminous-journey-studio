from pathlib import Path

from config.settings import AI_PROVIDER

from services.builder_service import BuilderService
from services.exporter_service import ExporterService

from services.stage1_service import Stage1Service
from services.stage2_service import Stage2Service
from services.stage3_service import Stage3Service
from services.stage4_service import Stage4Service


class ProductionEngine:

    def __init__(self):

        provider = AI_PROVIDER

        self.stage1 = Stage1Service(provider)
        self.stage2 = Stage2Service(provider)
        self.stage3 = Stage3Service(provider)
        self.stage4 = Stage4Service(provider)

    def run(
        self,
        gospel: str,
        language: str,
        audience: str,
        output_dir: Path,
    ):

        stage1 = self.stage1.generate(
            gospel,
            language,
            audience,
        )

        stage2 = self.stage2.generate(stage1)

        stage3 = self.stage3.generate(stage1)

        stage4 = self.stage4.generate(
            gospel,
            language,
            audience,
        )

        markdown = "\n\n".join(
            [
                stage1,
                stage2,
                stage3,
                stage4,
            ]
        )

        data = BuilderService.build(markdown)

        ExporterService.export(
            output_dir,
            data,
        )

        return data