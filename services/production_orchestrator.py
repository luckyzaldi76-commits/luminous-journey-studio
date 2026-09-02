from pathlib import Path
from typing import Iterable

from services.asset_pipeline import AssetPipeline
from services.gospel_input import GospelInput
from services.job_progress import JobProgressService
from services.job_queue import ProductionJobQueue
from services.job_recovery import JobRecoveryService
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
        job_progress=None,
    ):

        self.gospel_input = gospel_input

        self.multilingual_pipeline = (
            multilingual_pipeline
            or MultilingualGenerationPipeline()
        )

        self.job_queue = (
            job_queue
            or ProductionJobQueue()
        )

        self.job_progress = (
            job_progress
            or JobProgressService(
                self.job_queue
            )
        )

        self.asset_pipeline = (
            asset_pipeline
            or AssetPipeline()
        )

    @staticmethod
    def _normalize_gospel(
        gospel: str,
    ) -> str:

        if not isinstance(
            gospel,
            str,
        ):

            raise TypeError(
                "Gospel must be a string."
            )

        gospel = gospel.strip()

        if not gospel:

            raise ValueError(
                "Gospel cannot be empty."
            )

        return gospel

    def _prepare_gospel(
        self,
        gospel: str,
    ) -> str:

        if self.gospel_input is None:

            return self._normalize_gospel(
                gospel
            )

        normalized = (
            self.gospel_input.normalize(
                gospel
            )
        )

        if not isinstance(
            normalized,
            str,
        ):

            raise TypeError(
                "GospelInput.normalize() "
                "must return a string."
            )

        normalized = normalized.strip()

        if not normalized:

            raise ValueError(
                "Gospel cannot be empty."
            )

        return normalized

    def prepare(
        self,
        gospel: str,
        languages: Iterable[str],
        audience: str,
        output_dir: Path,
        workflow_name: str = "Daily Gospel",
    ) -> list[ProductionJob]:

        normalized_gospel = (
            self._prepare_gospel(
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

            if (
                self.job_queue.job_service.store
                is not None
            ):

                self.job_queue.job_service.store.save(
                    job
                )

            jobs.append(
                job
            )

        return jobs

    def _execute_job(
        self,
        job: ProductionJob,
    ) -> dict:

        metadata = job.result or {}

        gospel = metadata.get(
            "gospel"
        )

        language = metadata.get(
            "language"
        )

        audience = metadata.get(
            "audience"
        )

        workflow_name = metadata.get(
            "workflow",
            "Daily Gospel",
        )

        output_dir = metadata.get(
            "output_dir"
        )

        if not gospel:

            raise ValueError(
                "Job is missing gospel metadata."
            )

        if not language:

            raise ValueError(
                "Job is missing language metadata."
            )

        if audience is None:

            raise ValueError(
                "Job is missing audience metadata."
            )

        if not output_dir:

            raise ValueError(
                "Job is missing output_dir metadata."
            )

        output_dir = Path(
            output_dir
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        language_dir = output_dir

        result = (
            self.multilingual_pipeline
            .pipeline
            .generate(
                gospel=gospel,
                language=language,
                audience=audience,
                output_dir=language_dir,
                workflow_name=workflow_name,
            )
        )

        exported = (
            self.asset_pipeline.export(
                language_dir,
                language_dir.parent,
            )
        )

        return {
            "job_id": job.job_id,
            "language": language,
            "content": result,
            "assets": exported,
            "source_dir": str(
                language_dir
            ),
            "output_dir": str(
                language_dir.parent
            ),
        }

    def run(
        self,
        gospel: str,
        languages: Iterable[str],
        audience: str,
        output_dir: Path,
        workflow_name: str = "Daily Gospel",
    ) -> dict:

        normalized_gospel = (
            self._prepare_gospel(
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

        while not self.job_queue.empty():

            try:

                processed.append(
                    self.job_queue.run_next(
                        self._execute_job
                    )
                )

            except Exception:

                failed_job = (
                    self.job_queue.last_failed()
                    if hasattr(
                        self.job_queue,
                        "last_failed",
                    )
                    else None
                )

                if failed_job is not None:

                    processed.append(
                        failed_job
                    )

                continue

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

        progress = (
            self.job_progress.snapshot()
        )

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
            "progress": progress,
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

    def recover(
        self,
    ) -> dict:

        recovery = JobRecoveryService(
            self.job_queue.job_service
        )

        recoverable = (
            recovery.find_recoverable()
        )

        recovered = (
            recovery.recover(
                self._execute_job
            )
        )

        completed = [
            job
            for job in recovered
            if job.status == "completed"
        ]

        failed = [
            job
            for job in recovered
            if job.status == "failed"
        ]

        progress = (
            self.job_progress.snapshot()
        )

        return {
            "success": (
                len(failed) == 0
                and len(completed)
                == len(recoverable)
            ),
            "total_jobs": len(
                recoverable
            ),
            "recovered_jobs": len(
                recovered
            ),
            "completed_jobs": len(
                completed
            ),
            "failed_jobs": len(
                failed
            ),
            "progress": progress,
            "jobs": [
                {
                    "job_id": job.job_id,
                    "status": job.status,
                    "result": job.result,
                    "error": job.error,
                }
                for job in recovered
            ],
        }