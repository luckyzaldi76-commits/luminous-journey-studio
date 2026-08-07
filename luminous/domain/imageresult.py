from dataclasses import dataclass


@dataclass
class ImageResult:

    image_prompts: str

    def to_dict(self):

        return {

            "image_prompts": self.image_prompts,

        }