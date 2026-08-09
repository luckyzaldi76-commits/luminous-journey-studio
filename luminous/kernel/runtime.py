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

        self.event_bus.emit(
            "workflow.started",
            workflow.name,
        )

        start = time.perf_counter()

        try:

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

            result = TaskResult(

                task=workflow.name,

                success=True,

                duration=duration,

            )

            context.outputs["_runtime"] = {

                "success": True,

                "duration": duration,

                "workflow": workflow.name,

            }

            self.event_bus.emit(
                "workflow.finished",
                workflow.name,
            )

            return result

        except Exception as e:

            duration = (
                time.perf_counter()
                - start
            )

            result = TaskResult(

                task=workflow.name,

                success=False,

                duration=duration,

                message=str(e),

            )

            context.outputs["_runtime"] = {

                "success": False,

                "duration": duration,

                "workflow": workflow.name,

                "error": str(e),

            }

            self.event_bus.emit(
                "workflow.failed",
                workflow.name,
            )

            raise