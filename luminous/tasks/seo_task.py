from luminous.context.pipeline_context import PipelineContext
from luminous.tasks.base_task import BaseTask

from luminous.infrastructure.parsers.parser_service import ParserService
from services.stage2_service import Stage2Service


class SeoTask(BaseTask):

    name = "seo"

    version = "2.0"

    depends_on = (
        "script",
    )

    def __init__(self):

        self.stage = Stage2Service()

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
            "seo",
            ParserService.seo(
                response,
            ),
        )

        context.set(
            "hashtags",
            ParserService.hashtags(
                response,
            ),
        )

        return response