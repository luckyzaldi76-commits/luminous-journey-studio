from dataclasses import dataclass


@dataclass
class ScriptResult:

    title: str

    script: str

    def to_dict(self):

        return {

            "title": self.title,

            "script": self.script,

        }