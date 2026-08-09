from dataclasses import dataclass


@dataclass(slots=True)
class SeoResult:

    seo: str

    hashtags: str

    def to_dict(
        self,
    ) -> dict:

        return {

            "seo": self.seo,

            "hashtags": self.hashtags,

        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(

            seo=data.get(
                "seo",
                "",
            ),

            hashtags=data.get(
                "hashtags",
                "",
            ),

        )

    def __bool__(
        self,
    ) -> bool:

        return bool(

            self.seo.strip()

            and

            self.hashtags.strip()

        )