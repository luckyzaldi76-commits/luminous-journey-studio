from services.stage4_service import Stage4Service


class Stage4UseCase:

    def execute(
        self,
        gospel: str,
        language: str,
        audience: str,
    ):

        return Stage4Service().generate(
            gospel,
            language,
            audience,
        )