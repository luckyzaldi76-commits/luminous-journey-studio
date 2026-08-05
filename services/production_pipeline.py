from services.fallback_service import FallbackService

from infrastructure.log.logger import get_logger

logger = get_logger(__name__)


class ProductionPipeline:

    def __init__(self):

        self.ai = FallbackService()

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        logger.info("Production Pipeline Started")

        response = self.ai.generate(
            prompt,
            max_tokens=max_tokens,
        )

        logger.info("Production Pipeline Finished")

        return response