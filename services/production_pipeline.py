from pathlib import Path

from infrastructure.log.logger import get_logger
from services.ai_service import AIService
from services.builder_service import BuilderService
from services.exporter_service import ExporterService

logger = get_logger(__name__)


class ProductionPipeline:

    def __init__(self, provider_name: str):
        self.ai = AIService(provider_name)

    def generate(self, prompt: str, output_dir: Path):

        logger.info("Production Pipeline Started")

        response = self.ai.generate(prompt)

        data = BuilderService.build(response)

        ExporterService.export(output_dir, data)

        logger.info("Production Pipeline Finished")

        return data