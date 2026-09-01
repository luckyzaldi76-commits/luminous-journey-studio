from services.job_service import JobService


def main():

    service = JobService()

    job = service.create()

    assert job.job_id
    assert job.status == "queued"
    assert job.created_at
    assert job.attempts == 0
    assert job.last_error is None

    assert service.exists(
        job.job_id
    )

    started = service.start(
        job.job_id
    )

    assert started.status == "running"
    assert started.started_at
    assert started.attempts == 0

    service.record_attempt(
        job.job_id
    )

    current = service.get(
        job.job_id
    )

    assert current.attempts == 1

    service.record_error(
        job.job_id,
        "503 Service Unavailable",
    )

    current = service.get(
        job.job_id
    )

    assert current.attempts == 1
    assert current.last_error == (
        "503 Service Unavailable"
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

    assert completed.status == "completed"
    assert completed.attempts == 3

    assert completed.last_error == (
        "503 Service Unavailable"
    )

    assert completed.result == {
        "success": True,
    }

    snapshot = service.snapshot(
        job.job_id
    )

    assert snapshot["attempts"] == 3
    assert snapshot["last_error"] == (
        "503 Service Unavailable"
    )

    failed_job = service.create()

    service.start(
        failed_job.job_id
    )

    service.record_attempt(
        failed_job.job_id
    )

    failed = service.fail(
        failed_job.job_id,
        "401 Unauthorized",
    )

    assert failed.status == "failed"
    assert failed.attempts == 1
    assert failed.last_error == (
        "401 Unauthorized"
    )

    assert failed.error == (
        "401 Unauthorized"
    )

    try:

        service.record_attempt(
            "unknown-job"
        )

        raise AssertionError(
            "Unknown job should fail."
        )

    except KeyError:

        pass

    print("=" * 60)
    print("JOB ATTEMPT TRACKING TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()