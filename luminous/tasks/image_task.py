from luminous.context.pipeline_context import PipelineContext
from luminous.tasks.base_task import BaseTask

from luminous.infrastructure.parsers.parser_service import ParserService
from services.stage3_service import Stage3Service


class ImageTask(BaseTask):

    name = "image"

    version = "2.0"

    depends_on = (
        "script",
    )

    def __init__(self):

        self.stage = Stage3Service()

    def execute(
        self,
        context: PipelineContext,
    ):

        script = context.get(
            "script",
        )

        if not script:

            raise RuntimeError(
                "Script not found in PipelineContext."
            )

        response = self.stage.generate(
            script=script,
        )

        context.set(
            "image_prompts",
            ParserService.image_prompts(
                response,
            ),
        )

        return response