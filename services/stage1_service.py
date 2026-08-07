from config.settings import STAGE1_MAX_TOKENS

from services.fallback_service import FallbackService
from services.template_loader import TemplateLoader
from services.validator_service import ValidatorService


class Stage1Service:

    def __init__(self):

        self.ai = FallbackService()

    def build_prompt(
        self,
        gospel: str,
        language: str,
        audience: str,
    ) -> str:

        return TemplateLoader.load(
            "stage1.md",
            gospel=gospel,
            language=language,
            audience=audience,
        )

    def validate(
        self,
        response: str,
    ) -> None:

        ValidatorService.require_sections(
            response,
            "TITLE",
            "SCRIPT",
        )

    def generate(
        self,
        gospel: str,
        language: str,
        audience: str,
    ) -> str:

        prompt = self.build_prompt(
            gospel,
            language,
            audience,
        )

        response = self.ai.generate(
            prompt,
            max_tokens=STAGE1_MAX_TOKENS,
        )

        self.validate(
            response,
        )

        return response