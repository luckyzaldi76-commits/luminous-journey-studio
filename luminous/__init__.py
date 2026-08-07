from luminous.kernel.registry import WorkflowRegistry

from luminous.workflows.dailygospelworkflow import (
    DailyGospelWorkflow,
)

WorkflowRegistry.register(
    "daily_gospel",
    DailyGospelWorkflow,
)