class RetryPolicy:

    @staticmethod
    def should_retry(error: Exception) -> bool:

        message = str(error).lower()

        #
        # Do NOT retry
        #

        no_retry = (
            "429",
            "resource_exhausted",
            "quota",
            "402",
            "credit",
            "insufficient",
            "unauthorized",
            "401",
            "403",
            "invalid api key",
        )

        if any(item in message for item in no_retry):
            return False

        #
        # Retry
        #

        retry = (
            "500",
            "502",
            "503",
            "504",
            "timeout",
            "timed out",
            "connection",
            "temporarily",
            "unavailable",
        )

        if any(item in message for item in retry):
            return True

        #
        # default
        #

        return True