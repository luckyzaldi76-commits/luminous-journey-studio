from config.settings import STAGE2_MAX_TOKENS

from services.fallback_service import FallbackService
from services.template_loader import TemplateLoader
from services.validator_service import ValidatorService


class Stage2Service:

    def __init__(self):

        self.ai = FallbackService()

    def generate(
        self,
        script: str,
    ) -> str:

        prompt = TemplateLoader.load(
            "stage2.md",
            script=script,
        )

        response = self.ai.generate(
            prompt,
            max_tokens=STAGE2_MAX_TOKENS,
        )

        ValidatorService.require_sections(
            response,
            "SEO",
            "HASHTAGS",
        )

        return response