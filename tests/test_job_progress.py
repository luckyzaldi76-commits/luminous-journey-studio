from services.job_progress import JobProgressService


class FakeQueue:

    def __init__(self, snapshot):

        self._snapshot = snapshot

    def snapshot(self):

        return dict(
            self._snapshot
        )


def main():

    queue = FakeQueue(
        {
            "total": 3,
            "queued": 1,
            "running": 0,
            "completed": 1,
            "failed": 1,
            "remaining": 1,
            "success": False,
        }
    )

    service = JobProgressService(
        queue
    )

    progress = service.snapshot()

    assert progress["total"] == 3
    assert progress["queued"] == 1
    assert progress["running"] == 0
    assert progress["completed"] == 1
    assert progress["failed"] == 1
    assert progress["remaining"] == 1
    assert progress["success"] is False

    assert progress["finished"] is False

    assert progress["percentage"] == (
        66.67
    )

    assert progress["state"] == (
        "partial"
    )

    completed_queue = FakeQueue(
        {
            "total": 3,
            "queued": 0,
            "running": 0,
            "completed": 3,
            "failed": 0,
            "remaining": 0,
            "success": True,
        }
    )

    completed_service = (
        JobProgressService(
            completed_queue
        )
    )

    completed = (
        completed_service.snapshot()
    )

    assert completed["finished"] is True
    assert completed["percentage"] == 100.0
    assert completed["state"] == (
        "completed"
    )

    failed_queue = FakeQueue(
        {
            "total": 3,
            "queued": 0,
            "running": 0,
            "completed": 2,
            "failed": 1,
            "remaining": 0,
            "success": False,
        }
    )

    failed_service = (
        JobProgressService(
            failed_queue
        )
    )

    failed = (
        failed_service.snapshot()
    )

    assert failed["finished"] is True
    assert failed["percentage"] == 100.0
    assert failed["state"] == (
        "failed"
    )

    empty_queue = FakeQueue(
        {
            "total": 0,
            "queued": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
            "remaining": 0,
            "success": False,
        }
    )

    empty_service = (
        JobProgressService(
            empty_queue
        )
    )

    empty = (
        empty_service.snapshot()
    )

    assert empty["percentage"] == 0.0
    assert empty["finished"] is False
    assert empty["state"] == (
        "empty"
    )

    print("=" * 60)
    print(
        "JOB PROGRESS SERVICE TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
