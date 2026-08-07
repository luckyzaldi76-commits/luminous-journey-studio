from dataclasses import dataclass


@dataclass
class MetadataResult:

    metadata: str

    def to_dict(self):

        return {

            "metadata": self.metadata,

        }