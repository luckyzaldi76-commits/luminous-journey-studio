from pathlib import Path
from typing import Iterable, Optional

from services.asset_pipeline import AssetPipeline
from services.gospel_input import GospelInput
from services.job_queue import ProductionJobQueue
from services.job_service import ProductionJob
from services.multilingual_pipeline import (
    MultilingualGenerationPipeline,
)


class ProductionOrchestrator:

    def __init__(
        self,
        gospel_input=None,
        multilingual_pipeline=None,
        job_queue=None,
        asset_pipeline=None,
    ):

        self.gospel_input = (
            gospel_input
            or GospelInput()
        )

        self.multilingual_pipeline = (
            multilingual_pipeline
            or MultilingualGenerationPipeline()
        )

        self.job_queue = (
            job_queue
            or ProductionJobQueue()
        )

        self.asset_pipeline = (
            asset_pipeline
            or AssetPipeline()
        )

    def prepare(
        self,
        gospel: str,
        languages: Iterable[str],
        audience: str,
        output_dir: Path,
        workflow_name: str = "Daily Gospel",
    ) -> list[ProductionJob]:

        normalized_gospel = (
            self.gospel_input.normalize(
                gospel
            )
        )

        language_list = (
            self.multilingual_pipeline
            ._normalize_languages(
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

        jobs = []

        for language in language_list:

            job = self.job_queue.create()

            job.result = {
                "gospel": normalized_gospel,
                "language": language,
                "audience": audience,
                "workflow": workflow_name,
                "output_dir": str(
                    output_dir / language
                ),
            }

            jobs.append(job)

        return jobs

    def run(
        self,
        gospel: str,
        languages: Iterable[str],
        audience: str,
        output_dir: Path,
        workflow_name: str = "Daily Gospel",
    ) -> dict:

        normalized_gospel = (
            self.gospel_input.normalize(
                gospel
            )
        )

        language_list = (
            self.multilingual_pipeline
            ._normalize_languages(
                languages
            )
        )

        output_dir = Path(
            output_dir
        )

        jobs = self.prepare(
            gospel=normalized_gospel,
            languages=language_list,
            audience=audience,
            output_dir=output_dir,
            workflow_name=workflow_name,
        )

        processed = []

        def execute(job):

            metadata = job.result or {}

            language = metadata[
                "language"
            ]

            language_dir = (
                output_dir / language
            )

            result = (
                self.multilingual_pipeline.pipeline
                .generate(
                    gospel=normalized_gospel,
                    language=language,
                    audience=audience,
                    output_dir=language_dir,
                    workflow_name=workflow_name,
                )
            )

            asset_result = (
                self.asset_pipeline.export(
                    result,
                    language_dir,
                )
            )

            return {
                "job_id": job.job_id,
                "language": language,
                "content": result,
                "assets": asset_result,
            }

        while not self.job_queue.empty():

            processed.append(
                self.job_queue.run_next(
                    execute
                )
            )

        completed = [
            job
            for job in processed
            if job.status == "completed"
        ]

        failed = [
            job
            for job in processed
            if job.status == "failed"
        ]

        return {
            "success": (
                len(failed) == 0
                and len(completed)
                == len(jobs)
            ),
            "gospel": normalized_gospel,
            "audience": audience,
            "workflow": workflow_name,
            "languages": language_list,
            "total_jobs": len(jobs),
            "completed_jobs": len(completed),
            "failed_jobs": len(failed),
            "jobs": [
                {
                    "job_id": job.job_id,
                    "status": job.status,
                    "result": job.result,
                    "error": job.error,
                }
                for job in processed
            ],
            "output_dir": str(
                output_dir
            ),
        }
