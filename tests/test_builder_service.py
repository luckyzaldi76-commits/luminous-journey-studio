from luminous.context.pipeline_context import PipelineContext

from services.builder_service import BuilderService


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

        }

    )

    result = BuilderService.build(

        context,

    )

    assert result["title"]

    assert result["script"]

    assert result["seo"]

    assert result["hashtags"]

    assert result["image_prompts"]

    assert result["metadata"]

    print()

    print("=" * 60)

    print("BUILDER SERVICE TEST PASSED")

    print("=" * 60)

    print()

    for key, value in result.items():

        print("=" * 60)

        print(key.upper())

        print("-" * 60)

        print(value)


if __name__ == "__main__":

    main()