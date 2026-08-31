import tempfile
from pathlib import Path

from services.job_service import JobService
from services.job_store import PersistentJobStore


def main():

    with tempfile.TemporaryDirectory() as temp:

        path = Path(temp) / "jobs.json"

        store = PersistentJobStore(
            path
        )

        service = JobService(
            store=store
        )

        job = service.create()

        assert path.exists()
        assert store.exists(
            job.job_id
        )

        service.start(
            job.job_id
        )

        service.complete(
            job.job_id,
            {
                "gospel": "Lukas 5:33-39",
                "language": "IND",
            },
        )

        restored_store = (
            PersistentJobStore(path)
        )

        restored_service = JobService(
            store=restored_store
        )

        restored = restored_service.get(
            job.job_id
        )

        assert restored.status == (
            "completed"
        )

        assert restored.result == {
            "gospel": "Lukas 5:33-39",
            "language": "IND",
        }

        assert restored.created_at == (
            job.created_at
        )

        assert (
            restored.started_at
            is not None
        )

        assert (
            restored.completed_at
            is not None
        )

        assert (
            restored_store.count()
            == 1
        )

        assert (
            restored_store.delete(
                job.job_id
            )
            is True
        )

        assert (
            restored_store.exists(
                job.job_id
            )
            is False
        )

        assert (
            restored_store.delete(
                job.job_id
            )
            is False
        )

    print("=" * 60)
    print("JOB STORE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
