from services.job_queue import (
    ProductionJobQueue,
)


def main():

    queue = ProductionJobQueue()

    first = queue.create()
    second = queue.create()
    third = queue.create()

    assert queue.size() == 3
    assert not queue.empty()

    assert queue.peek().job_id == (
        first.job_id
    )

    assert queue.dequeue().job_id == (
        first.job_id
    )

    assert queue.dequeue().job_id == (
        second.job_id
    )

    assert queue.size() == 1

    assert queue.peek().job_id == (
        third.job_id
    )

    completed = queue.run_next(
        lambda job: {
            "job_id": job.job_id,
            "success": True,
        }
    )

    assert completed.job_id == (
        third.job_id
    )

    assert completed.status == (
        "completed"
    )

    assert completed.result == {
        "job_id": third.job_id,
        "success": True,
    }

    assert queue.empty()

    batch_queue = ProductionJobQueue()

    jobs = [
        batch_queue.create()
        for _ in range(3)
    ]

    processed = batch_queue.run_all(
        lambda job: {
            "job_id": job.job_id,
            "success": True,
        }
    )

    assert len(processed) == 3

    assert [
        job.job_id
        for job in processed
    ] == [
        job.job_id
        for job in jobs
    ]

    assert all(
        job.status == "completed"
        for job in processed
    )

    failure_queue = ProductionJobQueue()

    failed_job = failure_queue.create()

    failed = failure_queue.run_next(
        lambda job: (
            (_ for _ in ()).throw(
                RuntimeError(
                    "queue failure"
                )
            )
        )
    )

    assert failed.job_id == (
        failed_job.job_id
    )

    assert failed.status == (
        "failed"
    )

    assert failed.error == (
        "queue failure"
    )

    assert failure_queue.empty()

    retry_queue = ProductionJobQueue()

    retry_job = retry_queue.create()

    attempts = []

    def retry_executor(job):

        attempts.append(
            len(attempts) + 1
        )

        if len(attempts) < 3:

            raise RuntimeError(
                "503 temporary provider error"
            )

        return {
            "job_id": job.job_id,
            "attempts": len(attempts),
            "success": True,
        }

    retried = retry_queue.run_next(
        retry_executor,
        retries=3,
        delays=(0, 0, 0),
    )

    assert retried.job_id == (
        retry_job.job_id
    )

    assert retried.status == (
        "completed"
    )

    assert attempts == [
        1,
        2,
        3,
    ]

    assert retried.result == {
        "job_id": retry_job.job_id,
        "attempts": 3,
        "success": True,
    }

    permanent_queue = ProductionJobQueue()

    permanent_job = (
        permanent_queue.create()
    )

    permanent_attempts = []

    def permanent_executor(job):

        permanent_attempts.append(
            len(permanent_attempts) + 1
        )

        raise RuntimeError(
            "401 Unauthorized"
        )

    permanent = permanent_queue.run_next(
        permanent_executor,
        retries=3,
        delays=(0, 0, 0),
    )

    assert permanent.job_id == (
        permanent_job.job_id
    )

    assert permanent.status == (
        "failed"
    )

    assert permanent.error == (
        "401 Unauthorized"
    )

    assert permanent_attempts == [
        1,
    ]

    assert permanent_queue.empty()

    exhausted_queue = ProductionJobQueue()

    exhausted_job = (
        exhausted_queue.create()
    )

    exhausted_attempts = []

    def exhausted_executor(job):

        exhausted_attempts.append(
            len(exhausted_attempts) + 1
        )

        raise RuntimeError(
            "503 Service Unavailable"
        )

    exhausted = exhausted_queue.run_next(
        exhausted_executor,
        retries=3,
        delays=(0, 0, 0),
    )

    assert exhausted.job_id == (
        exhausted_job.job_id
    )

    assert exhausted.status == (
        "failed"
    )

    assert exhausted.error == (
        "503 Service Unavailable"
    )

    assert exhausted_attempts == [
        1,
        2,
        3,
    ]

    assert exhausted_queue.empty()

    print("=" * 60)
    print("JOB QUEUE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()