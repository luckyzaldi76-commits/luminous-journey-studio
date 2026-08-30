from pathlib import Path
from typing import Dict, Iterable

from config.settings import LANGUAGES
from services.content_pipeline import ProductionContentPipeline


class MultilingualGenerationPipeline:

    def __init__(
        self,
        pipeline=None,
    ):

        self.pipeline = (
            pipeline
            or ProductionContentPipeline()
        )

    def _normalize_languages(
        self,
        languages: Iterable[str],
    ) -> list[str]:

        if isinstance(
            languages,
            str,
        ):

            languages = (
                languages,
            )

        language_list = []

        for language in languages:

            if not isinstance(
                language,
                str,
            ):

                raise TypeError(
                    "Language must be a string."
                )

            language = language.strip().upper()

            if not language:
                continue

            if language not in LANGUAGES:

                raise ValueError(
                    f"Unsupported language: {language}"
                )

            if language not in language_list:

                language_list.append(
                    language
                )

        if not language_list:

            raise ValueError(
                "At least one language is required."
            )

        return language_list

    def generate(
        self,
        gospel: str,
        languages: Iterable[str],
        audience: str,
        output_dir: Path,
        workflow_name: str = "Daily Gospel",
    ) -> Dict[str, dict]:

        language_list = (
            self._normalize_languages(
                languages
            )
        )

        output_dir = Path(
            output_dir
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        results = {}

        for language in language_list:

            language_dir = (
                output_dir / language
            )

            results[language] = (
                self.pipeline.generate(
                    gospel=gospel,
                    language=language,
                    audience=audience,
                    output_dir=language_dir,
                    workflow_name=workflow_name,
                )
            )

        return results

    def generate_all(
        self,
        gospel: str,
        audience: str,
        output_dir: Path,
        workflow_name: str = "Daily Gospel",
    ) -> Dict[str, dict]:

        return self.generate(
            gospel=gospel,
            languages=LANGUAGES,
            audience=audience,
            output_dir=output_dir,
            workflow_name=workflow_name,
        )