from services.stage2_service import Stage2Service


class Stage2UseCase:

    def execute(
        self,
        response: str,
    ):

        return Stage2Service().generate(
            response,
        )