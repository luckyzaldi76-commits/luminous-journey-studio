import time
import requests

from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_URL,
    REQUEST_TIMEOUT,
    MAX_RETRY,
    OPENROUTER_MAX_TOKENS,
    OPENROUTER_TEMPERATURE,
)

from infrastructure.log.logger import get_logger

logger = get_logger(__name__)


def generate(
    prompt: str,
    max_tokens: int = OPENROUTER_MAX_TOKENS,
) -> str:

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Luminous Journey Studio",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "max_tokens": max_tokens,
        "temperature": OPENROUTER_TEMPERATURE,
    }

    logger.info("=" * 60)
    logger.info("OPENROUTER")
    logger.info("Model        : %s", OPENROUTER_MODEL)
    logger.info("Max Tokens   : %s", max_tokens)
    logger.info("Temperature  : %s", OPENROUTER_TEMPERATURE)

    for retry in range(MAX_RETRY):

        logger.info("Connecting... (%s/%s)", retry + 1, MAX_RETRY)

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        logger.info("HTTP %s", response.status_code)

        if response.status_code == 200:
            logger.info("Response received.")
            return response.json()["choices"][0]["message"]["content"]

        if response.status_code == 429:
            time.sleep(10)
            continue

        if response.status_code >= 500:
            time.sleep(5)
            continue

        raise RuntimeError(response.text)

    raise RuntimeError("OpenRouter request failed.")