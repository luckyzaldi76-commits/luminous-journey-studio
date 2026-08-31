import tempfile
from pathlib import Path

from services.job_recovery import JobRecoveryService
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

        service.start(
            job.job_id
        )

        restarted_service = JobService(
            store=PersistentJobStore(
                path
            )
        )

        recovery = JobRecoveryService(
            restarted_service
        )

        recoverable = (
            recovery.find_recoverable()
        )

        assert len(recoverable) == 1
        assert recoverable[0].job_id == (
            job.job_id
        )
        assert recoverable[0].status == (
            "running"
        )

        results = recovery.recover(
            lambda recovered_job: {
                "recovered": True,
                "job_id": recovered_job.job_id,
            }
        )

        assert len(results) == 1
        assert results[0].status == (
            "completed"
        )

        assert results[0].result == {
            "recovered": True,
            "job_id": job.job_id,
        }

        final_service = JobService(
            store=PersistentJobStore(
                path
            )
        )

        final_job = final_service.get(
            job.job_id
        )

        assert final_job.status == (
            "completed"
        )

        assert final_job.result == {
            "recovered": True,
            "job_id": job.job_id,
        }

        queued = final_service.create()

        queued_results = (
            JobRecoveryService(
                final_service
            ).recover(
                lambda recovered_job: {
                    "queued_recovered": True,
                    "job_id": recovered_job.job_id,
                }
            )
        )

        assert any(
            item.job_id == queued.job_id
            and item.status == "completed"
            for item in queued_results
        )

        failed_service = JobService(
            store=PersistentJobStore(
                Path(temp) / "failed.json"
            )
        )

        failed_job = failed_service.create()

        failed_recovery = JobRecoveryService(
            failed_service
        )

        failed_results = failed_recovery.recover(
            lambda recovered_job: (
                (_ for _ in ()).throw(
                    RuntimeError(
                        "recovery failure"
                    )
                )
            )
        )

        assert len(failed_results) == 1
        assert failed_results[0].job_id == (
            failed_job.job_id
        )
        assert failed_results[0].status == (
            "failed"
        )
        assert failed_results[0].error == (
            "recovery failure"
        )

    print("=" * 60)
    print("JOB RECOVERY TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
