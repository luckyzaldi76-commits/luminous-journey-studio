import os

import google.genai as genai

from dotenv import load_dotenv

from infrastructure.log.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash",
)


def generate(
    prompt: str,
) -> str:

    if not API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY belum dikonfigurasi."
        )

    client = genai.Client(
        api_key=API_KEY,
    )

    logger.info("=" * 60)
    logger.info("GEMINI")
    logger.info("Model : %s", MODEL)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return response.text


def stream(
    prompt: str,
):

    if not API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY belum dikonfigurasi."
        )

    client = genai.Client(
        api_key=API_KEY,
    )

    logger.info("=" * 60)
    logger.info("GEMINI STREAM")
    logger.info("Model : %s", MODEL)

    response = client.models.generate_content_stream(
        model=MODEL,
        contents=prompt,
    )

    for chunk in response:

        if chunk.text:

            yield chunk.text