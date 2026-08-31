from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import uuid4

from services.job_store import PersistentJobStore


@dataclass
class ProductionJob:

    job_id: str
    status: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    result: Optional[dict] = None


class JobService:

    VALID_STATUSES = {
        "queued",
        "running",
        "completed",
        "failed",
    }

    def __init__(
        self,
        store=None,
    ):

        self.store = store

        self._jobs: Dict[
            str,
            ProductionJob,
        ] = {}

        if self.store is not None:

            for data in self.store.all():

                job = ProductionJob(
                    **data
                )

                self._jobs[
                    job.job_id
                ] = job

    @staticmethod
    def _now() -> str:

        return (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

    def _persist(
        self,
        job: ProductionJob,
    ):

        if self.store is not None:

            self.store.save(
                job
            )

    def create(self) -> ProductionJob:

        job = ProductionJob(
            job_id=str(uuid4()),
            status="queued",
            created_at=self._now(),
        )

        self._jobs[
            job.job_id
        ] = job

        self._persist(
            job
        )

        return job

    def start(
        self,
        job_id: str,
    ) -> ProductionJob:

        job = self.get(
            job_id
        )

        self._require_status(
            job,
            {"queued"},
        )

        job.status = "running"
        job.started_at = self._now()

        self._persist(
            job
        )

        return job

    def complete(
        self,
        job_id: str,
        result: Optional[dict] = None,
    ) -> ProductionJob:

        job = self.get(
            job_id
        )

        self._require_status(
            job,
            {"running"},
        )

        job.status = "completed"
        job.completed_at = self._now()
        job.result = result

        self._persist(
            job
        )

        return job

    def fail(
        self,
        job_id: str,
        error: str,
    ) -> ProductionJob:

        job = self.get(
            job_id
        )

        self._require_status(
            job,
            {"queued", "running"},
        )

        job.status = "failed"
        job.completed_at = self._now()
        job.error = str(error)

        self._persist(
            job
        )

        return job

    def get(
        self,
        job_id: str,
    ) -> ProductionJob:

        if job_id in self._jobs:

            return self._jobs[
                job_id
            ]

        if self.store is not None:

            data = self.store.get(
                job_id
            )

            if data is not None:

                job = ProductionJob(
                    **data
                )

                self._jobs[
                    job.job_id
                ] = job

                return job

        raise KeyError(
            f"Unknown job: {job_id}"
        )

    def exists(
        self,
        job_id: str,
    ) -> bool:

        if job_id in self._jobs:

            return True

        if self.store is not None:

            return self.store.exists(
                job_id
            )

        return False

    def snapshot(
        self,
        job_id: str,
    ) -> dict:

        return asdict(
            self.get(
                job_id
            )
        )

    @classmethod
    def _require_status(
        cls,
        job: ProductionJob,
        allowed: set,
    ):

        if job.status not in allowed:

            raise ValueError(
                f"Invalid job transition: "
                f"{job.status}"
            )
