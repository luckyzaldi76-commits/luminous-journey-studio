import subprocess
import sys


TESTS = [
    "tests.test_ai",
    "tests.test_ai_service",
    "tests.test_builder_service",
    "tests.test_exporter_service",
    "tests.test_fallback",
    "tests.test_engine",
]


def run(test):

    print("=" * 60)
    print(test)
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", test],
    )

    if result.returncode != 0:

        print()
        print(f"FAILED : {test}")
        sys.exit(result.returncode)

    print()
    print(f"PASSED : {test}")
    print()


def main():

    print()
    print("=" * 60)
    print("LUMINOUS JOURNEY TEST SUITE")
    print("=" * 60)
    print()

    for test in TESTS:

        run(test)

    print("=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":

    main()