from datetime import datetime, timezone
from typing import Callable

from services.job_service import JobService, ProductionJob


class JobRecoveryService:

    def __init__(
        self,
        job_service: JobService,
    ):

        self.job_service = job_service

    @staticmethod
    def _parse_time(
        value: str,
    ) -> datetime:

        return datetime.fromisoformat(
            value
        )

    def find_recoverable(
        self,
    ) -> list[ProductionJob]:

        jobs = []

        if self.job_service.store is not None:

            data = self.job_service.store.all()

            for item in data:

                job = ProductionJob(
                    **item
                )

                if job.status in {
                    "queued",
                    "running",
                }:

                    jobs.append(job)

            return jobs

        for job in self.job_service._jobs.values():

            if job.status in {
                "queued",
                "running",
            }:

                jobs.append(job)

        return jobs

    def recover(
        self,
        executor: Callable[
            [ProductionJob],
            dict,
        ],
    ) -> list[ProductionJob]:

        recovered = []

        for job in self.find_recoverable():

            current = self.job_service.get(
                job.job_id
            )

            if current.status == "running":

                current.status = "queued"

                current.started_at = None

                if self.job_service.store is not None:

                    self.job_service.store.save(
                        current
                    )

            try:

                self.job_service.start(
                    current.job_id
                )

                result = executor(
                    current
                )

                completed = (
                    self.job_service.complete(
                        current.job_id,
                        result,
                    )
                )

                recovered.append(
                    completed
                )

            except Exception as error:

                self.job_service.fail(
                    current.job_id,
                    str(error),
                )

                recovered.append(
                    self.job_service.get(
                        current.job_id
                    )
                )

        return recovered
