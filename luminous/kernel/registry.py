from luminous.domain.workflow import Workflow


class WorkflowRegistry:

    _workflows: dict[str, type[Workflow]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        workflow: type[Workflow],
    ):

        key = name.strip().lower()

        if key in cls._workflows:

            raise RuntimeError(
                f"Workflow '{name}' already registered."
            )

        cls._workflows[key] = workflow

    @classmethod
    def unregister(
        cls,
        name: str,
    ):

        cls._workflows.pop(
            name.strip().lower(),
            None,
        )

    @classmethod
    def create(
        cls,
        name: str,
    ) -> Workflow:

        key = name.strip().lower()

        workflow = cls._workflows.get(
            key,
        )

        if workflow is None:

            available = ", ".join(
                cls.names(),
            )

            raise RuntimeError(

                f"Workflow '{name}' not found. "

                f"Available: {available}"

            )

        return workflow()

    @classmethod
    def get(
        cls,
        name: str,
    ):

        return cls._workflows.get(
            name.strip().lower(),
        )

    @classmethod
    def exists(
        cls,
        name: str,
    ) -> bool:

        return (
            name.strip().lower()
            in cls._workflows
        )

    @classmethod
    def names(
        cls,
    ) -> list[str]:

        return sorted(
            cls._workflows.keys(),
        )

    @classmethod
    def clear(
        cls,
    ):

        cls._workflows.clear()