class WorkflowRegistry:

    _workflows = {}

    @classmethod
    def register(
        cls,
        name: str,
        workflow,
    ):

        cls._workflows[name.lower()] = workflow

    @classmethod
    def create(
        cls,
        name: str,
    ):

        workflow = cls._workflows.get(
            name.lower(),
        )

        if workflow is None:

            raise RuntimeError(
                f"Workflow '{name}' not found."
            )

        return workflow()

    @classmethod
    def available(cls):

        return sorted(
            cls._workflows.keys()
        )