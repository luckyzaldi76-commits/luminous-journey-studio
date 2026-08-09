from concurrent.futures import ThreadPoolExecutor

from luminous.domain.executionnode import ExecutionNode


class Scheduler:

    def build(
        self,
        workflow,
    ):

        return [
            ExecutionNode.from_task(
                task,
            )
            for task in workflow.tasks
        ]

    def execute(
        self,
        nodes,
        context,
    ):

        completed = set()

        remaining = list(nodes)

        while remaining:

            ready = [
                node
                for node in remaining
                if node.ready(
                    completed,
                )
            ]

            if not ready:

                waiting = [
                    node.name
                    for node in remaining
                ]

                raise RuntimeError(
                    "Circular task dependency detected: "
                    + ", ".join(waiting)
                )

            with ThreadPoolExecutor(
                max_workers=max(
                    1,
                    len(ready),
                ),
            ) as executor:

                futures = {
                    executor.submit(
                        node.task.execute,
                        context,
                    ): node
                    for node in ready
                }

                for future, node in futures.items():

                    future.result()

                    node.mark_completed()

                    completed.add(
                        node.name,
                    )

                    remaining.remove(
                        node,
                    )