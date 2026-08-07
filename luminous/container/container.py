from services.stage1_service import Stage1Service
from services.stage2_service import Stage2Service
from services.stage3_service import Stage3Service
from services.stage4_service import Stage4Service


class Container:

    def __init__(self):

        self.stage1 = Stage1Service()

        self.stage2 = Stage2Service()

        self.stage3 = Stage3Service()

        self.stage4 = Stage4Service()