from services.validator_service import ValidatorService


class Stage4Service:

    def build_metadata(
        self,
        gospel: str,
        language: str,
        audience: str,
    ) -> str:

        return f"""# METADATA

AUTHOR=Luminous Journey

GOSPEL={gospel}

LANGUAGE={language}

AUDIENCE={audience}

VERSION=1.0

GENERATED_BY=Luminous Journey Studio
"""

    def validate(
        self,
        response: str,
    ) -> dict:

        return ValidatorService.require_sections(
            response,
            "METADATA",
        )

    def generate(
        self,
        gospel: str,
        language: str,
        audience: str,
    ) -> str:

        response = self.build_metadata(
            gospel,
            language,
            audience,
        )

        self.validate(
            response,
        )

        return response