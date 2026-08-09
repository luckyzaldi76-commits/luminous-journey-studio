from abc import ABC, abstractmethod


class BaseTask(ABC):

    name = ""

    version = "1.0"

    depends_on = ()

    @property
    def id(
        self,
    ) -> str:

        return self.name

    @property
    def dependencies(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            self.depends_on,
        )

    def validate(
        self,
    ) -> bool:

        if not self.name:

            raise RuntimeError(
                f"{self.__class__.__name__} has no task name."
            )

        return True

    @abstractmethod
    def execute(
        self,
        context,
    ):
        """
        Execute task using PipelineContext.
        """
        raise NotImplementedError

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(name='{self.name}', "

            f"version='{self.version}')"

        )