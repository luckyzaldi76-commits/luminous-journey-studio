from google import genai
from google.genai import types

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

from infrastructure.log.logger import get_logger


logger = get_logger(__name__)


def _client():

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY,
    )


def _config(
    max_tokens: int,
):

    return types.GenerateContentConfig(

        max_output_tokens=max_tokens,

        thinking_config=types.ThinkingConfig(

            thinking_level="minimal",

        ),

    )


def generate(
    prompt: str,
    max_tokens: int = 512,
) -> str:

    logger.info("=" * 60)

    logger.info("GEMINI")

    logger.info(
        "Model : %s",
        GEMINI_MODEL,
    )

    logger.info(
        "Max Tokens : %s",
        max_tokens,
    )

    logger.info(
        "Thinking : minimal",
    )

    client = _client()

    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=prompt,

        config=_config(
            max_tokens,
        ),

    )

    text = response.text

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


def stream(
    prompt: str,
    max_tokens: int = 512,
):

    logger.info("=" * 60)

    logger.info("GEMINI STREAM")

    logger.info(
        "Model : %s",
        GEMINI_MODEL,
    )

    logger.info(
        "Max Tokens : %s",
        max_tokens,
    )

    logger.info(
        "Thinking : minimal",
    )

    client = _client()

    response = client.models.generate_content_stream(

        model=GEMINI_MODEL,

        contents=prompt,

        config=_config(
            max_tokens,
        ),

    )

    for chunk in response:

        text = getattr(
            chunk,
            "text",
            None,
        )

        if text:

            yield text