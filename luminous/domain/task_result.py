from dataclasses import dataclass, field


@dataclass(slots=True)
class TaskResult:

    task: str

    success: bool = True

    duration: float = 0.0

    message: str = ""

    data: dict = field(
        default_factory=dict,
    )

    def to_dict(
        self,
    ) -> dict:

        return {

            "task": self.task,

            "success": self.success,

            "duration": self.duration,

            "message": self.message,

            "data": self.data,

        }

    @classmethod
    def ok(
        cls,
        task: str,
        duration: float = 0.0,
        data: dict | None = None,
    ):

        return cls(

            task=task,

            success=True,

            duration=duration,

            data=data or {},

        )

    @classmethod
    def failed(
        cls,
        task: str,
        message: str,
        duration: float = 0.0,
        data: dict | None = None,
    ):

        return cls(

            task=task,

            success=False,

            duration=duration,

            message=message,

            data=data or {},

        )

    def __bool__(
        self,
    ) -> bool:

        return self.success