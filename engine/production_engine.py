from pathlib import Path

from services.production_pipeline import ProductionPipeline
from services.prompt_builder import PromptBuilder


class ProductionEngine:

    def __init__(self, provider="openrouter"):
        self.pipeline = ProductionPipeline(provider)

    def run(
        self,
        template: Path,
        output_dir: Path,
        **kwargs,
    ):

        prompt = PromptBuilder.build(
            template,
            **kwargs,
        )

        return self.pipeline.generate(
            prompt,
            output_dir,
        )