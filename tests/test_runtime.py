from luminous.context.pipeline_context import PipelineContext

from luminous.kernel.event_bus import EventBus
from luminous.kernel.runtime import Runtime
from luminous.kernel.scheduler import Scheduler

from luminous.workflows.dailygospelworkflow import (
    DailyGospelWorkflow,
)


def main():

    context = PipelineContext(

        gospel="Matthew 14:13-21",

        language="English",

        audience="Adults",

    )

    workflow = DailyGospelWorkflow()

    runtime = Runtime(

        scheduler=Scheduler(),

        event_bus=EventBus(),

    )

    result = runtime.run(

        workflow,

        context,

    )

    assert result.success

    assert context.outputs["title"]

    assert context.outputs["script"]

    assert context.outputs["seo"]

    assert context.outputs["hashtags"]

    assert context.outputs["image_prompts"]

    assert context.outputs["metadata"]

    assert "_runtime" in context.outputs

    print()

    print("=" * 60)

    print("RUNTIME TEST PASSED")

    print("=" * 60)

    print()

    print(result.to_dict())


if __name__ == "__main__":

    main()