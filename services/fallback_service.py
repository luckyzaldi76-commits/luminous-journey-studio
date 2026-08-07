from config.settings import (
    AI_PROVIDER,
    USE_MOCK,
)

from infrastructure.log.logger import get_logger
from services.ai_service import AIService

logger = get_logger(__name__)


class FallbackService:

    def __init__(self):

        if AI_PROVIDER.lower() == "gemini":

            self.providers = [
                "gemini",
            ]

        elif AI_PROVIDER.lower() == "openrouter":

            self.providers = [
                "openrouter",
            ]

        else:

            # AUTO MODE
            self.providers = [
                "gemini",
                "openrouter",
            ]

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
    ) -> str:

        # ==========================================
        # MOCK MODE
        # ==========================================

        if USE_MOCK:

            logger.info("Using Mock Provider")

            print("▶ Provider : Mock")

            print("✓ Mock succeeded\n")

            return """
# TITLE

Mock Title

# SCRIPT

This is a mock response.

# SEO

Mock SEO

# HASHTAGS

#mock

# IMAGE_PROMPTS

Mock image prompt.

# METADATA

AUTHOR=Mock
"""

        errors = []

        for provider in self.providers:

            try:

                logger.info(
                    "Trying provider: %s",
                    provider,
                )

                print(
                    f"▶ Provider : {provider.capitalize()}"
                )

                ai = AIService(provider)

                result = ai.generate(
                    prompt,
                    max_tokens=max_tokens,
                )

                logger.info(
                    "%s succeeded",
                    provider,
                )

                print(
                    f"✓ {provider.capitalize()} succeeded\n"
                )

                return result

            except Exception as e:

                message = str(e).splitlines()[0]

                logger.warning(
                    "%s failed: %s",
                    provider,
                    message,
                )

                print(
                    f"✗ {provider.capitalize()} failed"
                )

                print(
                    f"  Reason : {message}\n"
                )

                errors.append(
                    f"{provider.capitalize()}: {message}"
                )

        raise RuntimeError(
            "All AI providers failed.\n\n"
            + "\n".join(errors)
        )

    def stream(
        self,
        prompt: str,
        max_tokens: int = 512,
    ):

        errors = []

        for provider in self.providers:

            try:

                logger.info(
                    "Trying provider: %s",
                    provider,
                )

                ai = AIService(provider)

                yield from ai.stream(
                    prompt,
                    max_tokens=max_tokens,
                )

                logger.info(
                    "%s succeeded",
                    provider,
                )

                return

            except Exception as e:

                message = str(e).splitlines()[0]

                logger.warning(
                    "%s failed: %s",
                    provider,
                    message,
                )

                errors.append(
                    f"{provider.capitalize()}: {message}"
                )

        raise RuntimeError(
            "All AI providers failed.\n\n"
            + "\n".join(errors)
        )