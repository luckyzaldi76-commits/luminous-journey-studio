from dataclasses import dataclass


@dataclass
class SeoResult:

    seo: str

    hashtags: str

    def to_dict(self):

        return {

            "seo": self.seo,

            "hashtags": self.hashtags,

        }