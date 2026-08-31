from pathlib import Path
from typing import Iterable

from services.job_queue import ProductionJobQueue
from services.job_service import ProductionJob
from services.multilingual_pipeline import (
    MultilingualGenerationPipeline,
)


class MultilingualJobPipeline:

    def __init__(
        self,
        multilingual_pipeline=None,
        job_queue=None,
    ):

        self.pipeline = (
            multilingual_pipeline
            or MultilingualGenerationPipeline()
        )

        self.queue = (
            job_queue
            or ProductionJobQueue()
        )

    def enqueue(
        self,
        gospel: str,
        languages: Iterable[str],
        audience: str,
        output_dir: Path,
        workflow_name: str = "Daily Gospel",
    ) -> list[ProductionJob]:

        language_list = (
            self.pipeline._normalize_languages(
                languages
            )
        )

        jobs = []

        for language in language_list:

            job = self.queue.create()

            job.result = {
                "gospel": gospel,
                "language": language,
                "audience": audience,
                "output_dir": str(
                    Path(output_dir) / language
                ),
                "workflow": workflow_name,
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

        language_list = (
            self.pipeline._normalize_languages(
                languages
            )
        )

        output_dir = Path(
            output_dir
        )

        jobs = self.enqueue(
            gospel=gospel,
            languages=language_list,
            audience=audience,
            output_dir=output_dir,
            workflow_name=workflow_name,
        )

        results = []

        def execute(job):

            metadata = job.result or {}

            language = metadata[
                "language"
            ]

            result = self.pipeline.pipeline.generate(
                gospel=gospel,
                language=language,
                audience=audience,
                output_dir=(
                    output_dir / language
                ),
                workflow_name=workflow_name,
            )

            return result

        while not self.queue.empty():

            completed = self.queue.run_next(
                execute
            )

            results.append(
                completed
            )

        return {
            "gospel": gospel,
            "audience": audience,
            "workflow": workflow_name,
            "languages": language_list,
            "jobs": [
                {
                    "job_id": job.job_id,
                    "status": job.status,
                    "language": (
                        job.result.get("language")
                        if job.result
                        else None
                    ),
                    "result": job.result,
                    "error": job.error,
                }
                for job in results
            ],
            "success": all(
                job.status == "completed"
                for job in results
            ),
        }
