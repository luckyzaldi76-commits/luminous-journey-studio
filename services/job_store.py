import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional


class PersistentJobStore:

    def __init__(self, path):

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        job,
    ):

        jobs = self._load()

        jobs[job.job_id] = asdict(
            job
        )

        self._write(
            jobs
        )

        return job

    def get(
        self,
        job_id: str,
    ) -> Optional[dict]:

        jobs = self._load()

        return jobs.get(
            job_id
        )

    def exists(
        self,
        job_id: str,
    ) -> bool:

        return (
            job_id
            in self._load()
        )

    def delete(
        self,
        job_id: str,
    ) -> bool:

        jobs = self._load()

        if job_id not in jobs:

            return False

        del jobs[job_id]

        self._write(
            jobs
        )

        return True

    def all(self) -> list[dict]:

        return list(
            self._load().values()
        )

    def count(self) -> int:

        return len(
            self._load()
        )

    def _load(self) -> dict:

        if not self.path.exists():

            return {}

        content = self.path.read_text(
            encoding="utf-8"
        )

        if not content.strip():

            return {}

        try:

            data = json.loads(
                content
            )

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Invalid job store: {error}"
            ) from error

        if not isinstance(
            data,
            dict,
        ):

            raise ValueError(
                "Job store must contain an object."
            )

        return data

    def _write(
        self,
        jobs: dict,
    ):

        temporary = self.path.with_suffix(
            self.path.suffix + ".tmp"
        )

        temporary.write_text(
            json.dumps(
                jobs,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        temporary.replace(
            self.path
        )
