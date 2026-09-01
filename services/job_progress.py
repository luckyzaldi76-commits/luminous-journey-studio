class JobProgressService:

    def __init__(
        self,
        queue,
    ):

        self.queue = queue

    def snapshot(
        self,
    ) -> dict:

        snapshot = dict(
            self.queue.snapshot()
        )

        total = snapshot["total"]
        completed = snapshot["completed"]
        failed = snapshot["failed"]
        remaining = snapshot["remaining"]

        if total == 0:

            percentage = 0.0
            finished = False
            state = "empty"

        else:

            percentage = round(
                (
                    (completed + failed)
                    / total
                ) * 100,
                2,
            )

            finished = (
                remaining == 0
            )

            if not finished:

                state = "partial"

            elif failed > 0:

                state = "failed"

            else:

                state = "completed"

        return {
            **snapshot,
            "percentage": percentage,
            "finished": finished,
            "state": state,
        }
