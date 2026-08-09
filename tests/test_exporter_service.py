from pathlib import Path

from luminous.context.pipeline_context import PipelineContext

from services.builder_service import BuilderService
from services.exporter_service import ExporterService


def main():

    context = PipelineContext(

        gospel="Matthew 14:13-21",

        language="English",

        audience="Adults",

    )

    context.outputs.update(

        {

            "title": "Walking with Jesus",

            "script": "This is script.",

            "seo": "SEO Description",

            "hashtags": "#faith\n#jesus",

            "image_prompts": "Prompt 1\nPrompt 2",

            "metadata": {

                "Author": "Luminous",

            },

            "_runtime": {

                "success": True,

            },

        }

    )

    data = BuilderService.build(

        context,

    )

    output = Path(

        "exports/test",

    )

    ExporterService.export(

        output,

        data,

    )

    assert (

        output / "script.txt"

    ).exists()

    assert (

        output / "response.md"

    ).exists()

    assert (

        output / "seo.json"

    ).exists()

    assert (

        output / "metadata.json"

    ).exists()

    assert (

        output / "image_prompts.md"

    ).exists()

    assert (

        output / "runtime.json"

    ).exists()

    print()

    print("=" * 60)

    print("EXPORTER SERVICE TEST PASSED")

    print("=" * 60)


if __name__ == "__main__":

    main()