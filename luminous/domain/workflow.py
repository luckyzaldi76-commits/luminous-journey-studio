from dataclasses import dataclass, field

from luminous.tasks.base_task import BaseTask


@dataclass
class Workflow:

    name: str

    version: str = "1.0"

    description: str = ""

    tasks: list[BaseTask] = field(
        default_factory=list
    )