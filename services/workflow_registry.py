from typing import Type

from luminous.workflows.dailygospelworkflow import (
    DailyGospelWorkflow,
)


class WorkflowRegistry:

    def __init__(self):

        self._workflows = {}

        self.register(
            "Daily Gospel",
            DailyGospelWorkflow,
        )

        self.register(
            "daily_gospel",
            DailyGospelWorkflow,
        )

    def register(
        self,
        name: str,
        workflow_class: Type,
    ):

        key = name.strip().lower()

        if not key:
            raise ValueError(
                "Workflow name cannot be empty."
            )

        if not isinstance(
            workflow_class,
            type,
        ):
            raise TypeError(
                "workflow_class must be a class."
            )

        self._workflows[key] = workflow_class

    def get(
        self,
        name: str,
    ):

        key = name.strip().lower()

        if key not in self._workflows:
            raise ValueError(
                f"Unknown workflow: {name}"
            )

        return self._workflows[key]

    def create(
        self,
        name: str,
    ):

        return self.get(name)()

    def names(self):

        return tuple(
            sorted(
                self._workflows.keys()
            )
        )


workflow_registry = WorkflowRegistry()