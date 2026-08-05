from services.ai_service import AIService

from infrastructure.log.logger import get_logger

logger = get_logger(__name__)


class FallbackService:

    def __init__(self):

        self.providers = [
            "gemini",
            "openrouter",
        ]

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:

        last_error = None

        for provider in self.providers:

            try:

                logger.info(f"Trying {provider}")

                ai = AIService(provider)

                return ai.generate(
                    prompt,
                    max_tokens=max_tokens,
                )

            except Exception as e:

                logger.warning(f"{provider} failed: {e}")

                last_error = e

        raise RuntimeError(
            f"All AI providers failed.\n{last_error}"
        )

    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        last_error = None

        for provider in self.providers:

            try:

                logger.info(f"Trying {provider}")

                ai = AIService(provider)

                yield from ai.stream(
                    prompt,
                    max_tokens=max_tokens,
                )

                return

            except Exception as e:

                logger.warning(f"{provider} failed: {e}")

                last_error = e

        raise RuntimeError(
            f"All AI providers failed.\n{last_error}"
        )