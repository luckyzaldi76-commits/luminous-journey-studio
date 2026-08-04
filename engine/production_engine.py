from pathlib import Path

from services.production_pipeline import ProductionPipeline


class ProductionEngine:

    def __init__(self, provider="openrouter"):
        self.pipeline = ProductionPipeline(provider)

    def run(self, prompt: str, output_dir: Path):

        return self.pipeline.generate(
            prompt=prompt,
            output_dir=output_dir,
        )