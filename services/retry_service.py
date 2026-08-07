import time

from infrastructure.log.logger import get_logger

logger = get_logger(__name__)


class RetryService:

    @staticmethod
    def execute(
        func,
        retries: int = 3,
        delays: tuple = (2, 5, 10),
    ):

        last_error = None

        for attempt in range(retries):

            try:

                return func()

            except Exception as e:

                last_error = e

                if attempt == retries - 1:
                    break

                delay = delays[min(attempt, len(delays) - 1)]

                logger.warning(
                    "Retry %s/%s in %s sec: %s",
                    attempt + 1,
                    retries,
                    delay,
                    str(e),
                )

                print(
                    f"⚠ Retry {attempt + 1}/{retries} "
                    f"in {delay}s..."
                )

                time.sleep(delay)

        raise last_error