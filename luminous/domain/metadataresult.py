from dataclasses import dataclass


@dataclass(slots=True)
class MetadataResult:

    metadata: str

    def to_dict(
        self,
    ) -> dict:

        return {

            "metadata": self.metadata,

        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(

            metadata=data.get(
                "metadata",
                "",
            ),

        )

    def __bool__(
        self,
    ) -> bool:

        return bool(

            self.metadata.strip()

        )