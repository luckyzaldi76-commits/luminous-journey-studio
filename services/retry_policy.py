class RetryPolicy:

    NO_RETRY = (
        "400",
        "401",
        "402",
        "403",
        "404",
        "405",
        "406",
        "409",
        "422",
        "429",
        "quota",
        "resource_exhausted",
        "insufficient",
        "credit",
        "invalid api key",
        "invalid_api_key",
        "unauthorized",
        "permission",
        "forbidden",
        "content policy",
        "safety",
    )

    RETRY = (
        "408",
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
        "server error",
    )

    @classmethod
    def should_retry(
        cls,
        error: Exception,
    ) -> bool:

        message = str(
            error
        ).lower()

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