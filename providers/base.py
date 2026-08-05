from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:
        pass

    @abstractmethod
    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):
        pass