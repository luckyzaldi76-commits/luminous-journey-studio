from luminous.context.pipeline_context import PipelineContext


class BuilderService:

    REQUIRED = (

        "title",

        "script",

        "seo",

        "hashtags",

        "image_prompts",

        "metadata",

    )

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

        missing = []

        for field in cls.REQUIRED:

            value = outputs.get(
                field,
            )

            if value is None:

                missing.append(
                    field,
                )

                continue

            if isinstance(
                value,
                str,
            ):

                if not value.strip():

                    missing.append(
                        field,
                    )

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

            "_runtime": outputs.get(
                "_runtime",
                {},
            ),

        }