import logging

_INITIALIZED = False


def get_logger(name: str) -> logging.Logger:
    global _INITIALIZED

    if not _INITIALIZED:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )
        _INITIALIZED = True

    return logging.getLogger(name)