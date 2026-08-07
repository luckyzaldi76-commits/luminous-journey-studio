from luminous.context.pipeline_context import PipelineContext
from luminous.tasks.base_task import BaseTask

from services.parser_service import ParserService
from services.stage1_service import Stage1Service


class ScriptTask(BaseTask):

    name = "script"

    version = "2.0"

    def __init__(self):

        self.stage = Stage1Service()

    def execute(
        self,
        context: PipelineContext,
    ):

        response = self.stage.generate(
            gospel=context.gospel,
            language=context.language,
            audience=context.audience,
        )

        context.outputs["title"] = ParserService.title(
            response,
        )

        context.outputs["script"] = ParserService.script(
            response,
        )

        return response