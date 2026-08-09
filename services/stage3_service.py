from config.settings import STAGE3_MAX_TOKENS

from luminous.infrastructure.templates.template_loader import (
    TemplateLoader,
)

from services.fallback_service import FallbackService
from services.validator_service import ValidatorService


class Stage3Service:

    def __init__(self):

        self.ai = FallbackService()

    def build_prompt(
        self,
        script: str,
    ) -> str:

        return TemplateLoader.load(
            "stage3.md",
            script=script,
        )

    def validate(
        self,
        response: str,
    ) -> dict:

        return ValidatorService.require_sections(
            response,
            "IMAGE_PROMPTS",
        )

    def generate(
        self,
        script: str,
    ) -> str:

        prompt = self.build_prompt(
            script,
        )

        response = self.ai.generate(
            prompt,
            max_tokens=STAGE3_MAX_TOKENS,
        )

        self.validate(
            response,
        )

        return response