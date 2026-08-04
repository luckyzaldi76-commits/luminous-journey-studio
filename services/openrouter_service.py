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


def generate(prompt: str) -> str:

    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY belum dikonfigurasi.")

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
        "max_tokens": OPENROUTER_MAX_TOKENS,
        "temperature": OPENROUTER_TEMPERATURE,
    }

    logger.info("=" * 60)
    logger.info("OPENROUTER")
    logger.info("Model        : %s", OPENROUTER_MODEL)
    logger.info("Max Tokens   : %s", OPENROUTER_MAX_TOKENS)
    logger.info("Temperature  : %s", OPENROUTER_TEMPERATURE)

    for retry in range(MAX_RETRY):

        logger.info("Connecting... (%s/%s)", retry + 1, MAX_RETRY)

        try:

            response = requests.post(
                OPENROUTER_URL,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )

            logger.info("HTTP %s", response.status_code)

            # SUCCESS
            if response.status_code == 200:

                result = response.json()

                logger.info("Response received.")

                return result["choices"][0]["message"]["content"]

            # RATE LIMIT
            if response.status_code == 429:

                logger.warning("Rate limit. Retry 10 detik...")

                time.sleep(10)

                continue

            # SERVER ERROR
            if response.status_code >= 500:

                logger.warning("Server Error. Retry 5 detik...")

                time.sleep(5)

                continue

            # PAYMENT REQUIRED
            if response.status_code == 402:

                logger.error(response.text)

                raise RuntimeError(
                    "OpenRouter credits tidak mencukupi atau max_tokens terlalu besar."
                )

            # AUTH ERROR
            if response.status_code == 401:

                logger.error(response.text)

                raise RuntimeError("OPENROUTER_API_KEY tidak valid.")

            # FORBIDDEN
            if response.status_code == 403:

                logger.error(response.text)

                raise RuntimeError("Akses OpenRouter ditolak.")

            # NOT FOUND
            if response.status_code == 404:

                logger.error(response.text)

                raise RuntimeError("Model OpenRouter tidak ditemukan.")

            logger.error(response.text)

            response.raise_for_status()

        except requests.RequestException as ex:

            logger.exception(ex)

            if retry == MAX_RETRY - 1:
                raise

            time.sleep(5)

    raise RuntimeError("OpenRouter gagal setelah maksimum retry.")