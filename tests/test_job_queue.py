from services.job_queue import ProductionJobQueue


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

    try:

        failure_queue.run_next(
            lambda job: (
                (_ for _ in ()).throw(
                    RuntimeError(
                        "queue failure"
                    )
                )
            )
        )

        raise AssertionError(
            "Executor failure should propagate."
        )

    except RuntimeError as error:

        assert str(error) == (
            "queue failure"
        )

    assert (
        failure_queue.job_service
        .get(failed_job.job_id)
        .status
        == "failed"
    )

    assert failure_queue.empty()

    print("=" * 60)
    print("JOB QUEUE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
