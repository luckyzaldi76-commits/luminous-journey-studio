from services.retry_policy import RetryPolicy


def main():

    assert RetryPolicy.should_retry(
        RuntimeError("401 Unauthorized")
    ) is False

    assert RetryPolicy.should_retry(
        RuntimeError("402 insufficient credits")
    ) is False

    assert RetryPolicy.should_retry(
        RuntimeError("429 RESOURCE_EXHAUSTED")
    ) is False

    assert RetryPolicy.should_retry(
        RuntimeError("500 Internal Server Error")
    ) is True

    assert RetryPolicy.should_retry(
        RuntimeError("502 Bad Gateway")
    ) is True

    assert RetryPolicy.should_retry(
        RuntimeError("503 Service Unavailable")
    ) is True

    assert RetryPolicy.should_retry(
        RuntimeError("connection timeout")
    ) is True

    assert RetryPolicy.should_retry(
        RuntimeError("unexpected provider error")
    ) is True

    assert RetryPolicy.retry_delay(0) == 2
    assert RetryPolicy.retry_delay(1) == 5
    assert RetryPolicy.retry_delay(2) == 10
    assert RetryPolicy.retry_delay(3) == 20
    assert RetryPolicy.retry_delay(4) == 30
    assert RetryPolicy.retry_delay(99) == 30

    print(
        "PASS : authentication/quota errors -> no retry"
    )

    print(
        "PASS : transient server errors -> retry"
    )

    print(
        "PASS : timeout/connection errors -> retry"
    )

    print(
        "PASS : retry delays are correct"
    )

    print()

    print("=" * 60)

    print(
        "RETRY POLICY TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()