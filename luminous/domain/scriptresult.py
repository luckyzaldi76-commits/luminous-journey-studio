from dataclasses import dataclass


@dataclass(slots=True)
class ScriptResult:

    title: str

    script: str

    def to_dict(
        self,
    ) -> dict:

        return {

            "title": self.title,

            "script": self.script,

        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(

            title=data.get(
                "title",
                "",
            ),

            script=data.get(
                "script",
                "",
            ),

        )

    def __bool__(
        self,
    ) -> bool:

        return bool(

            self.title.strip()

            and

            self.script.strip()

        )