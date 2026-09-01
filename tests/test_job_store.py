import tempfile
from pathlib import Path

from services.job_service import JobService
from services.job_store import PersistentJobStore


def main():

    with tempfile.TemporaryDirectory() as temp:

        store_path = (
            Path(temp)
            / "jobs.json"
        )

        store = PersistentJobStore(
            store_path
        )

        service = JobService(
            store=store
        )

        job = service.create()

        service.start(
            job.job_id
        )

        service.record_attempt(
            job.job_id
        )

        service.record_error(
            job.job_id,
            "503 Service Unavailable",
        )

        service.record_attempt(
            job.job_id
        )

        service.record_error(
            job.job_id,
            "503 Service Unavailable",
        )

        service.record_attempt(
            job.job_id
        )

        completed = service.complete(
            job.job_id,
            {
                "success": True,
            },
        )

        assert completed.status == (
            "completed"
        )

        assert completed.attempts == 3

        assert completed.last_error == (
            "503 Service Unavailable"
        )

        assert store.exists(
            job.job_id
        )

        raw = store.get(
            job.job_id
        )

        assert raw["attempts"] == 3

        assert raw["last_error"] == (
            "503 Service Unavailable"
        )

        restored_service = JobService(
            store=store
        )

        restored = (
            restored_service.get(
                job.job_id
            )
        )

        assert restored.status == (
            "completed"
        )

        assert restored.attempts == 3

        assert restored.last_error == (
            "503 Service Unavailable"
        )

        assert restored.result == {
            "success": True,
        }

        snapshot = (
            restored_service.snapshot(
                job.job_id
            )
        )

        assert snapshot["attempts"] == 3

        assert snapshot["last_error"] == (
            "503 Service Unavailable"
        )

    print("=" * 60)
    print(
        "PERSISTENT JOB ATTEMPT TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()