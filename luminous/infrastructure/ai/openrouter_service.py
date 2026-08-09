import json

import requests

from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_MAX_TOKENS,
    OPENROUTER_MODEL,
    OPENROUTER_TEMPERATURE,
    OPENROUTER_URL,
    REQUEST_TIMEOUT,
)

from infrastructure.log.logger import get_logger


logger = get_logger(__name__)


def _headers() -> dict:

    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Luminous Journey Studio",
    }


def _payload(
    prompt: str,
    max_tokens: int,
    stream: bool = False,
) -> dict:

    return {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "max_tokens": max_tokens,
        "temperature": OPENROUTER_TEMPERATURE,
        "stream": stream,
    }


def generate(
    prompt: str,
    max_tokens: int = OPENROUTER_MAX_TOKENS,
) -> str:

    logger.info("=" * 60)

    logger.info("OPENROUTER")

    logger.info(
        "Model : %s",
        OPENROUTER_MODEL,
    )

    response = requests.post(
        OPENROUTER_URL,
        headers=_headers(),
        json=_payload(
            prompt,
            max_tokens,
            stream=False,
        ),
        timeout=REQUEST_TIMEOUT,
    )

    if not response.ok:

        raise RuntimeError(
            response.text
        )

    body = response.json()

    return (
        body["choices"][0]
        ["message"]
        ["content"]
    )


def stream(
    prompt: str,
    max_tokens: int = OPENROUTER_MAX_TOKENS,
):

    logger.info("=" * 60)

    logger.info("OPENROUTER STREAM")

    response = requests.post(
        OPENROUTER_URL,
        headers=_headers(),
        json=_payload(
            prompt,
            max_tokens,
            stream=True,
        ),
        timeout=REQUEST_TIMEOUT,
        stream=True,
    )

    if not response.ok:

        raise RuntimeError(
            response.text
        )

    for line in response.iter_lines():

        if not line:
            continue

        text = line.decode(
            "utf-8"
        )

        if not text.startswith(
            "data: "
        ):
            continue

        payload = text[6:]

        if payload == "[DONE]":
            break

        try:

            obj = json.loads(
                payload
            )

            delta = (
                obj["choices"][0]
                .get(
                    "delta",
                    {},
                )
                .get(
                    "content",
                )
            )

            if delta:
                yield delta

        except Exception:
            continue