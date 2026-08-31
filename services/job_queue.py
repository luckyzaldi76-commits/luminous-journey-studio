from collections import deque
from typing import Callable, Optional

from services.job_service import JobService, ProductionJob


class ProductionJobQueue:

    def __init__(
        self,
        job_service=None,
    ):

        self.job_service = (
            job_service
            or JobService()
        )

        self._queue = deque()

    def enqueue(
        self,
        job_id: str,
    ) -> ProductionJob:

        job = self.job_service.get(
            job_id
        )

        if job.status != "queued":

            raise ValueError(
                "Only queued jobs can be enqueued."
            )

        if job_id in self._queue:

            raise ValueError(
                f"Job already queued: {job_id}"
            )

        self._queue.append(
            job_id
        )

        return job

    def create(
        self,
    ) -> ProductionJob:

        job = self.job_service.create()

        self.enqueue(
            job.job_id
        )

        return job

    def size(self) -> int:

        return len(self._queue)

    def empty(self) -> bool:

        return not self._queue

    def peek(self) -> Optional[ProductionJob]:

        if not self._queue:

            return None

        return self.job_service.get(
            self._queue[0]
        )

    def dequeue(self) -> ProductionJob:

        if not self._queue:

            raise IndexError(
                "Production job queue is empty."
            )

        job_id = self._queue.popleft()

        return self.job_service.get(
            job_id
        )

    def run_next(
        self,
        executor: Callable[
            [ProductionJob],
            dict,
        ],
    ) -> ProductionJob:

        job = self.dequeue()

        self.job_service.start(
            job.job_id
        )

        try:

            result = executor(
                job
            )

            self.job_service.complete(
                job.job_id,
                result,
            )

        except Exception as error:

            self.job_service.fail(
                job.job_id,
                str(error),
            )

            raise

        return self.job_service.get(
            job.job_id
        )

    def run_all(
        self,
        executor: Callable[
            [ProductionJob],
            dict,
        ],
    ) -> list[ProductionJob]:

        results = []

        while not self.empty():

            results.append(
                self.run_next(
                    executor
                )
            )

        return results
