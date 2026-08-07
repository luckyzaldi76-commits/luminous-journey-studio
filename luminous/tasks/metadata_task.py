from luminous.context.pipeline_context import PipelineContext
from luminous.tasks.base_task import BaseTask

from services.parser_service import ParserService
from services.stage4_service import Stage4Service


class MetadataTask(BaseTask):

    name = "metadata"

    version = "2.0"

    def __init__(self):

        self.stage = Stage4Service()

    def execute(
        self,
        context: PipelineContext,
    ):

        response = self.stage.generate(

            gospel=context.gospel,

            language=context.language,

            audience=context.audience,

        )

        context.outputs["metadata"] = (
            ParserService.metadata(
                response,
            )
        )

        return response