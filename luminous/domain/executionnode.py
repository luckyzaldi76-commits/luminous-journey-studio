from dataclasses import dataclass

from luminous.tasks.base_task import BaseTask


@dataclass
class ExecutionNode:

    task: BaseTask