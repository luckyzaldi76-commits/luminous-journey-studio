from dataclasses import dataclass


@dataclass(slots=True)
class ImageResult:

    image_prompts: str

    def to_dict(
        self,
    ) -> dict:

        return {

            "image_prompts": self.image_prompts,

        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(

            image_prompts=data.get(
                "image_prompts",
                "",
            ),

        )

    def __bool__(
        self,
    ) -> bool:

        return bool(

            self.image_prompts.strip()

        )