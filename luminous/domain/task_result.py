from dataclasses import dataclass, field


@dataclass(slots=True)
class TaskResult:

    task: str

    success: bool = True

    duration: float = 0.0

    message: str = ""

    data: dict = field(default_factory=dict)