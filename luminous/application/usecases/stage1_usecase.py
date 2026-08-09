from services.stage1_service import Stage1Service


class Stage1UseCase:

    def execute(
        self,
        gospel: str,
        language: str,
        audience: str,
    ):

        return Stage1Service().generate(
            gospel=gospel,
            language=language,
            audience=audience,
        )