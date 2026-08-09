class RetryPolicy:

    NO_RETRY = (
        "401",
        "402",
        "403",
        "404",
        "429",
        "quota",
        "resource_exhausted",
        "insufficient",
        "credit",
        "invalid api key",
        "unauthorized",
        "permission",
        "forbidden",
    )

    RETRY = (
        "408",
        "409",
        "425",
        "500",
        "502",
        "503",
        "504",
        "timeout",
        "timed out",
        "connection",
        "connection reset",
        "connection aborted",
        "temporarily",
        "temporary",
        "unavailable",
        "internal server error",
        "bad gateway",
        "gateway timeout",
    )

    @classmethod
    def should_retry(
        cls,
        error: Exception,
    ) -> bool:

        message = str(error).lower()

        for item in cls.NO_RETRY:

            if item in message:

                return False

        for item in cls.RETRY:

            if item in message:

                return True

        return True

    @classmethod
    def retry_delay(
        cls,
        attempt: int,
    ) -> int:

        delays = (
            2,
            5,
            10,
            20,
            30,
        )

        return delays[
            min(
                attempt,
                len(delays) - 1,
            )
        ]