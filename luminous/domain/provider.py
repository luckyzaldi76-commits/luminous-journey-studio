from dataclasses import dataclass


@dataclass(slots=True)
class Provider:

    name: str

    model: str = ""

    enabled: bool = True

    priority: int = 0

    def to_dict(
        self,
    ) -> dict:

        return {

            "name": self.name,

            "model": self.model,

            "enabled": self.enabled,

            "priority": self.priority,

        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(

            name=data.get(
                "name",
                "",
            ),

            model=data.get(
                "model",
                "",
            ),

            enabled=data.get(
                "enabled",
                True,
            ),

            priority=data.get(
                "priority",
                0,
            ),

        )

    def __bool__(
        self,
    ) -> bool:

        return self.enabled