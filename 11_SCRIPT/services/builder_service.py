from builders.ppt_builder import builder as ppt_builder
from builders.script_builder import builder as script_builder
from builders.image_builder import builder as image_builder
from builders.seo_builder import builder as seo_builder
from builders.metadata_builder import builder as metadata_builder
from builders.manifest_builder import builder as manifest_builder

from services.logger_service import logger_service


class BuilderService:

    def build_all(
        self,
        data,
        output_dir
    ):

        logger_service.log(
            output_dir,
            "Generate PPT"
        )

        ppt_builder.build(
            data,
            output_dir / "presentation.pptx"
        )

        logger_service.log(
            output_dir,
            "Generate Script"
        )

        script_builder.build(
            data,
            output_dir / "script.txt"
        )

        logger_service.log(
            output_dir,
            "Generate Image Prompt"
        )

        image_builder.build(
            data,
            output_dir / "image_prompts.md"
        )

        logger_service.log(
            output_dir,
            "Generate SEO"
        )

        seo_builder.build(
            data,
            output_dir / "seo.json"
        )

        logger_service.log(
            output_dir,
            "Generate Metadata"
        )

        metadata_builder.build(
            data,
            output_dir / "metadata.json"
        )

        manifest_builder.build(
            output_dir
        )

        logger_service.log(
            output_dir,
            "Production Finished")


builder_service = BuilderService()