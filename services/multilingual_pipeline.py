from pathlib import Path
from typing import Dict, Iterable

from services.content_pipeline import ProductionContentPipeline


class MultilingualGenerationPipeline:

    def __init__(self, pipeline=None):
        self.pipeline = pipeline or ProductionContentPipeline()

    def generate(
        self,
        gospel: str,
        languages: Iterable[str],
        audience: str,
        output_dir: Path,
        workflow_name: str = "Daily Gospel",
    ) -> Dict[str, dict]:

        language_list = [
            language.strip()
            for language in languages
            if language.strip()
        ]

        if not language_list:
            raise ValueError("At least one language is required.")

        results = {}

        for language in language_list:

            language_dir = Path(output_dir) / language

            results[language] = self.pipeline.generate(
                gospel=gospel,
                language=language,
                audience=audience,
                output_dir=language_dir,
                workflow_name=workflow_name,
            )

        return results
