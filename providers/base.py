from abc import ABC, abstractmethod


class AIProvider(ABC):

    name = "provider"

    @property
    def model(
        self,
    ) -> str:

        return self.name

    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:
        """
        Generate a complete response.
        """
        raise NotImplementedError

    @abstractmethod
    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):
        """
        Stream a response.
        """
        raise NotImplementedError

    def supports_stream(
        self,
    ) -> bool:

        return True

    def __str__(
        self,
    ) -> str:

        return self.name

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', "
            f"model='{self.model}')"
        )