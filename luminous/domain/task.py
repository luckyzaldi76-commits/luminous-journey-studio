from dataclasses import dataclass, field


@dataclass(slots=True)
class Task:

    name: str

    version: str = "1.0"

    description: str = ""

    depends_on: tuple[str, ...] = field(
        default_factory=tuple,
    )

    enabled: bool = True

    def to_dict(
        self,
    ) -> dict:

        return {

            "name": self.name,

            "version": self.version,

            "description": self.description,

            "depends_on": list(
                self.depends_on,
            ),

            "enabled": self.enabled,

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

            version=data.get(
                "version",
                "1.0",
            ),

            description=data.get(
                "description",
                "",
            ),

            depends_on=tuple(
                data.get(
                    "depends_on",
                    [],
                )
            ),

            enabled=data.get(
                "enabled",
                True,
            ),

        )

    def __bool__(
        self,
    ) -> bool:

        return self.enabled