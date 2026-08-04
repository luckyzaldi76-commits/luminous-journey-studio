from pathlib import Path

from services.production_pipeline import ProductionPipeline
from services.prompt_loader import PromptLoader


class ProductionEngine:

    def __init__(self, provider="openrouter"):
        self.pipeline = ProductionPipeline(provider)

    def run(
        self,
        prompt_file: Path,
        output_dir: Path,
    ):

        prompt = PromptLoader.load(prompt_file)

        return self.pipeline.generate(
            prompt,
            output_dir,
        )