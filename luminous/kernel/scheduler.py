from concurrent.futures import ThreadPoolExecutor

from luminous.tasks.script_task import ScriptTask


class Scheduler:

    def build(
        self,
        workflow,
    ):

        return workflow.tasks

    def execute(
        self,
        tasks,
        context,
    ):

        #
        # ScriptTask harus selalu dulu
        #

        script_task = None

        parallel = []

        for task in tasks:

            if isinstance(
                task,
                ScriptTask,
            ):

                script_task = task

            else:

                parallel.append(
                    task,
                )

        #
        # Stage 1
        #

        if script_task:

            script_task.execute(
                context,
            )

        #
        # Stage 2+
        #

        with ThreadPoolExecutor(

            max_workers=len(parallel),

        ) as executor:

            futures = [

                executor.submit(

                    task.execute,

                    context,

                )

                for task in parallel

            ]

            for future in futures:

                future.result()