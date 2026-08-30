from services.job_service import JobService


def main():

    service = JobService()

    job = service.create()

    assert job.job_id
    assert job.status == "queued"
    assert job.created_at

    assert service.exists(
        job.job_id
    )

    started = service.start(
        job.job_id
    )

    assert started.status == "running"
    assert started.started_at

    result = {
        "gospel": "Lukas 5:33-39",
        "language": "IND",
    }

    completed = service.complete(
        job.job_id,
        result,
    )

    assert completed.status == "completed"
    assert completed.completed_at
    assert completed.result == result

    snapshot = service.snapshot(
        job.job_id
    )

    assert snapshot["job_id"] == (
        job.job_id
    )

    assert snapshot["status"] == (
        "completed"
    )

    failed_job = service.create()

    service.fail(
        failed_job.job_id,
        "test failure",
    )

    assert (
        service.get(
            failed_job.job_id
        ).status
        == "failed"
    )

    try:

        service.get(
            "unknown-job"
        )

        raise AssertionError(
            "Unknown job should fail."
        )

    except KeyError:

        pass

    try:

        service.complete(
            failed_job.job_id
        )

        raise AssertionError(
            "Invalid transition should fail."
        )

    except ValueError:

        pass

    print("=" * 60)
    print("JOB SERVICE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
