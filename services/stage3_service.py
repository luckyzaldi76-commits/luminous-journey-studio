from config.settings import STAGE3_MAX_TOKENS

from services.fallback_service import FallbackService
from services.template_loader import TemplateLoader
from services.validator_service import ValidatorService


class Stage3Service:

    def __init__(self):

        self.ai = FallbackService()

    def generate(
        self,
        script: str,
    ) -> str:

        prompt = TemplateLoader.load(
            "stage3.md",
            script=script,
        )

        response = self.ai.generate(
            prompt,
            max_tokens=STAGE3_MAX_TOKENS,
        )

        ValidatorService.require_sections(
            response,
            "IMAGE_PROMPTS",
        )

        return response