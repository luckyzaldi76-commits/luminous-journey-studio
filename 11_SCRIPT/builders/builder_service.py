from builders.ppt_builder import builder as ppt_builder
from builders.script_builder import builder as script_builder
from builders.image_builder import builder as image_builder
from builders.seo_builder import builder as seo_builder


class BuilderService:

    def build_all(
        self,
        data,
        base_filename
    ):

        print()
        print("=" * 60)
        print("BUILDERS")
        print("=" * 60)

        print("Generate PPT...")

        ppt_builder.build(
            data,
            f"{base_filename}.pptx"
        )

        print("Generate Script...")

        script_builder.build(
            data,
            f"{base_filename}.txt"
        )

        print("Generate Image Prompt...")

        image_builder.build(
            data,
            f"{base_filename}.md"
        )

        print("Generate SEO...")

        seo_builder.build(
            data,
            f"{base_filename}.json"
        )

        print()
        print("All Builders Finished.")


builder_service = BuilderService()