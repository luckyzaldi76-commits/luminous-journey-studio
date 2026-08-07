import logging
from pathlib import Path

_INITIALIZED = False


def get_logger(name: str) -> logging.Logger:

    global _INITIALIZED

    if not _INITIALIZED:

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        root = logging.getLogger()
        root.setLevel(logging.INFO)

        root.handlers.clear()

        #
        # Console
        #

        console = logging.StreamHandler()

        console.setLevel(logging.WARNING)

        console.setFormatter(formatter)

        #
        # app.log
        #

        app_file = logging.FileHandler(
            log_dir / "app.log",
            encoding="utf-8",
        )

        app_file.setLevel(logging.INFO)

        app_file.setFormatter(formatter)

        #
        # error.log
        #

        error_file = logging.FileHandler(
            log_dir / "error.log",
            encoding="utf-8",
        )

        error_file.setLevel(logging.ERROR)

        error_file.setFormatter(formatter)

        root.addHandler(console)
        root.addHandler(app_file)
        root.addHandler(error_file)

        #
        # Reduce noisy third-party loggers
        #

        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
        logging.getLogger("google").setLevel(logging.WARNING)
        logging.getLogger("google_genai").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        _INITIALIZED = True

    return logging.getLogger(name)