from luminous.domain.workflow import Workflow

from luminous.tasks.script_task import ScriptTask
from luminous.tasks.seo_task import SeoTask
from luminous.tasks.image_task import ImageTask
from luminous.tasks.metadata_task import MetadataTask


class DailyGospelWorkflow(Workflow):

    def __init__(self):

        super().__init__(

            name="Daily Gospel",

            version="1.0",

            description="Standard Daily Gospel Workflow",

            tasks=[

                ScriptTask(),

                SeoTask(),

                ImageTask(),

                MetadataTask(),

            ],

        )

    def validate(
        self,
    ):

        if not self.tasks:

            raise RuntimeError(
                "Workflow has no tasks."
            )

        names = set()

        for task in self.tasks:

            if not task.name:

                raise RuntimeError(
                    "Task name cannot be empty."
                )

            if task.name in names:

                raise RuntimeError(
                    f"Duplicate task: {task.name}"
                )

            names.add(
                task.name,
            )

        return True