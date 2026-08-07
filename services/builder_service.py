from luminous.context.pipeline_context import PipelineContext


class BuilderService:

    REQUIRED = [

        "title",

        "script",

        "seo",

        "hashtags",

        "image_prompts",

        "metadata",

    ]

    @classmethod
    def build(
        cls,
        context: PipelineContext,
    ) -> dict:

        if not isinstance(
            context,
            PipelineContext,
        ):

            raise TypeError(
                "BuilderService.build() expects PipelineContext."
            )

        outputs = context.outputs

        missing = [

            field

            for field in cls.REQUIRED

            if not outputs.get(field)

        ]

        if missing:

            raise RuntimeError(

                "Builder missing field(s): "

                + ", ".join(missing)

            )

        return {

            "title": outputs["title"],

            "script": outputs["script"],

            "seo": outputs["seo"],

            "hashtags": outputs["hashtags"],

            "image_prompts": outputs["image_prompts"],

            "metadata": outputs["metadata"],

        }