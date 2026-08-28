import subprocess
import sys


TESTS = (
    "tests.test_runtime",
    "tests.test_engine",
    "tests.test_template_loader",
    "tests.test_builder_service",
    "tests.test_exporter_service",
    "tests.test_ai_service",
    "tests.test_fallback",
    "tests.test_fallback_routing",
    "tests.test_provider_failover",
    "tests.test_retry_policy",
    "tests.test_provider_health",
    "tests.test_health_aware_failover",
    "tests.test_provider_cooldowns",
    "tests.test_provider_health_persistence",
)


def run(
    test: str,
):

    print("=" * 60)
    print(test)
    print("=" * 60)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            test,
        ]
    )

    if result.returncode != 0:

        print()
        print(f"FAILED : {test}")

        sys.exit(
            result.returncode,
        )

    print()
    print(f"PASSED : {test}")
    print()


def main():

    print()
    print("=" * 60)
    print("LUMINOUS JOURNEY TEST SUITE")
    print("=" * 60)
    print()

    passed = 0

    for test in TESTS:

        run(test)

        passed += 1

    print("=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)
    print(f"Executed : {passed}")
    print()


if __name__ == "__main__":

    main()