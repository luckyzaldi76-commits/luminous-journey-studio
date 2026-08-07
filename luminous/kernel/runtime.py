import time

from luminous.domain.task_result import TaskResult


class Runtime:

    def __init__(
        self,
        scheduler,
        event_bus,
    ):

        self.scheduler = scheduler

        self.event_bus = event_bus

    def run(
        self,
        workflow,
        context,
    ):

        start = time.perf_counter()

        self.event_bus.emit(
            "workflow.started",
            workflow.name,
        )

        tasks = self.scheduler.build(
            workflow,
        )

        self.scheduler.execute(
            tasks,
            context,
        )

        duration = (
            time.perf_counter()
            - start
        )

        context.outputs["_runtime"] = {

            "duration": duration,

            "success": True,

        }

        self.event_bus.emit(
            "workflow.finished",
            workflow.name,
        )

        return TaskResult(

            task=workflow.name,

            success=True,

            duration=duration,

        )