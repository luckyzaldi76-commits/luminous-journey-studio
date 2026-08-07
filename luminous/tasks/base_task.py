from abc import ABC, abstractmethod

from luminous.context.pipeline_context import PipelineContext
from luminous.domain.task_result import TaskResult


class BaseTask(ABC):

    name = ""

    @abstractmethod
    def execute(
        self,
        context: PipelineContext,
    ) -> TaskResult:
        ...