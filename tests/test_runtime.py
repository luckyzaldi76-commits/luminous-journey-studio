from luminous.context.pipeline_context import PipelineContext

from luminous.domain.workflow import Workflow

from luminous.kernel.runtime import Runtime
from luminous.kernel.scheduler import Scheduler
from luminous.kernel.event_bus import EventBus

from luminous.tasks.script_task import ScriptTask
from luminous.tasks.seo_task import SeoTask
from luminous.tasks.image_task import ImageTask
from luminous.tasks.metadata_task import MetadataTask


def main():

    context = PipelineContext(

        gospel="Matthew 14:13-21",

        language="English",

        audience="Adults",

    )

    workflow = Workflow(

        name="Daily Gospel",

        tasks=[

            ScriptTask(),

            SeoTask(),

            ImageTask(),

            MetadataTask(),

        ],

    )

    runtime = Runtime(

        scheduler=Scheduler(),

        event_bus=EventBus(),

    )

    runtime.run(

        workflow,

        context,

    )

    print("=" * 60)
    print("RUNTIME OK")
    print("=" * 60)
    print()

    print("OUTPUTS")
    print(context.outputs.keys())


if __name__ == "__main__":
    main()