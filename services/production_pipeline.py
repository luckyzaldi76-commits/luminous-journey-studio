from services.ai_service import AIService
from infrastructure.log.logger import get_logger

logger = get_logger(__name__)


class ProductionPipeline:

    def __init__(self, provider_name: str):
        self.ai = AIService(provider_name)

    def generate(self, prompt: str) -> str:
        logger.info("Production Pipeline Started")

        response = self.ai.generate(prompt)

        logger.info("Production Pipeline Finished")

        return response