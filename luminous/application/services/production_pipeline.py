from luminous.application.usecases.stage1_usecase import Stage1UseCase
from luminous.application.usecases.stage2_usecase import Stage2UseCase
from luminous.application.usecases.stage3_usecase import Stage3UseCase
from luminous.application.usecases.stage4_usecase import Stage4UseCase


class ProductionPipeline:

    def __init__(self):

        self.stage1 = Stage1UseCase()
        self.stage2 = Stage2UseCase()
        self.stage3 = Stage3UseCase()
        self.stage4 = Stage4UseCase()

    def execute(
        self,
        gospel: str,
        language: str,
        audience: str,
    ):

        stage1 = self.stage1.execute(
            gospel,
            language,
            audience,
        )

        stage2 = self.stage2.execute(
            stage1,
        )

        stage3 = self.stage3.execute(
            stage1,
        )

        stage4 = self.stage4.execute(
            gospel,
            language,
            audience,
        )

        return {
            "stage1": stage1,
            "stage2": stage2,
            "stage3": stage3,
            "stage4": stage4,
        }