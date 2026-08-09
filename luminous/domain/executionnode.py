from dataclasses import dataclass, field

from luminous.tasks.base_task import BaseTask


@dataclass(slots=True)
class ExecutionNode:

    task: BaseTask

    completed: bool = False

    skipped: bool = False

    running: bool = False

    duration: float = 0.0

    error: str = ""

    dependencies: tuple[str, ...] = field(
        default_factory=tuple,
    )

    @classmethod
    def from_task(
        cls,
        task: BaseTask,
    ):

        return cls(

            task=task,

            dependencies=tuple(
                task.dependencies,
            ),

        )

    @property
    def name(
        self,
    ) -> str:

        return self.task.name

    def mark_running(
        self,
    ):

        self.running = True

    def mark_completed(
        self,
        duration: float = 0.0,
    ):

        self.running = False

        self.completed = True

        self.duration = duration

    def mark_failed(
        self,
        message: str,
        duration: float = 0.0,
    ):

        self.running = False

        self.completed = False

        self.error = message

        self.duration = duration

    def mark_skipped(
        self,
    ):

        self.running = False

        self.skipped = True

    def ready(
        self,
        completed: set[str],
    ) -> bool:

        return all(

            dependency in completed

            for dependency in self.dependencies

        )