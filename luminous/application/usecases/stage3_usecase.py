from services.stage3_service import Stage3Service


class Stage3UseCase:

    def execute(
        self,
        response: str,
    ):

        return Stage3Service().generate(
            response,
        )