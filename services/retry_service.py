import time

from infrastructure.log.logger import get_logger
from services.retry_policy import RetryPolicy


logger = get_logger(__name__)


class RetryService:

    DEFAULT_RETRIES = 3

    DEFAULT_DELAYS = (
        2,
        5,
        10,
    )

    @classmethod
    def execute(
        cls,
        func,
        retries: int | None = None,
        delays: tuple | None = None,
        retry_policy=RetryPolicy,
    ):

        retries = (
            cls.DEFAULT_RETRIES
            if retries is None
            else retries
        )

        delays = (
            cls.DEFAULT_DELAYS
            if delays is None
            else delays
        )

        last_error = None

        for attempt in range(retries):

            try:

                return func()

            except Exception as error:

                last_error = error

                if not retry_policy.should_retry(
                    error,
                ):

                    raise

                if attempt >= retries - 1:

                    raise

                delay = (
                    delays[
                        min(
                            attempt,
                            len(delays) - 1,
                        )
                    ]
                )

                logger.warning(
                    "Retry attempt %s/%s after error: %s. "
                    "Waiting %s seconds.",
                    attempt + 1,
                    retries,
                    error,
                    delay,
                )

                time.sleep(
                    delay,
                )

        raise last_error