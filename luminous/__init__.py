from luminous.kernel.registry import WorkflowRegistry

from luminous.workflows.dailygospelworkflow import (
    DailyGospelWorkflow,
)

__version__ = "0.5.0"

__all__ = [

    "DailyGospelWorkflow",

    "WorkflowRegistry",

]


def register_workflows():

    if not WorkflowRegistry.exists(

        "daily_gospel",

    ):

        WorkflowRegistry.register(

            "daily_gospel",

            DailyGospelWorkflow,

        )


register_workflows()