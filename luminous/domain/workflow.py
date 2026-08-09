from dataclasses import dataclass, field

from luminous.tasks.base_task import BaseTask


@dataclass(slots=True)
class Workflow:

    name: str

    tasks: list[BaseTask] = field(
        default_factory=list,
    )

    version: str = "1.0"

    description: str = ""

    def add_task(
        self,
        task: BaseTask,
    ):

        self.tasks.append(
            task,
        )

    def remove_task(
        self,
        name: str,
    ):

        self.tasks = [

            task

            for task in self.tasks

            if task.name != name

        ]

    def get_task(
        self,
        name: str,
    ):

        for task in self.tasks:

            if task.name == name:

                return task

        return None

    def has_task(
        self,
        name: str,
    ) -> bool:

        return self.get_task(
            name,
        ) is not None

    def task_names(
        self,
    ) -> list[str]:

        return [

            task.name

            for task in self.tasks

        ]

    def validate(
        self,
    ):

        if not self.tasks:

            raise RuntimeError(
                "Workflow has no tasks."
            )

        names = set()

        for task in self.tasks:

            if not task.name:

                raise RuntimeError(
                    "Task name cannot be empty."
                )

            if task.name in names:

                raise RuntimeError(
                    f"Duplicate task: {task.name}"
                )

            names.add(
                task.name,
            )

        for task in self.tasks:

            dependencies = getattr(
                task,
                "depends_on",
                [],
            )

            for dependency in dependencies:

                if dependency not in names:

                    raise RuntimeError(

                        f"Task '{task.name}' depends on unknown task '{dependency}'."

                    )

        return True

    def __len__(
        self,
    ) -> int:

        return len(
            self.tasks,
        )

    def __iter__(
        self,
    ):

        return iter(
            self.tasks,
        )

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.has_task(
            name,
        )