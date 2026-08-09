from dataclasses import dataclass, field


@dataclass(slots=True)
class Result:

    success: bool = True

    message: str = ""

    data: dict = field(
        default_factory=dict,
    )

    def to_dict(
        self,
    ) -> dict:

        return {

            "success": self.success,

            "message": self.message,

            "data": self.data,

        }

    @classmethod
    def ok(
        cls,
        data: dict | None = None,
    ):

        return cls(

            success=True,

            data=data or {},

        )

    @classmethod
    def failed(
        cls,
        message: str,
        data: dict | None = None,
    ):

        return cls(

            success=False,

            message=message,

            data=data or {},

        )

    def __bool__(
        self,
    ) -> bool:

        return self.success