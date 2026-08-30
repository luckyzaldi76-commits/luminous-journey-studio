import subprocess
from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent.parent
)


REQUIRED_FILES = (
    "config/settings.py",
    "services/ai_service.py",
    "services/provider_health.py",
    "services/retry_policy.py",
    "providers/factory.py",
    "tests/run_all.py",
    "tests/test_release_gate.py",
    "tests/test_repository_audit.py",
    "tests/test_e2e_production_flow.py",
    "tests/test_full_pipeline_e2e.py",
    "tests/test_full_system_validation.py",
)


def git(*args):

    return subprocess.run(
        [
            "git",
            *args,
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )


def main():

    for relative_path in REQUIRED_FILES:

        path = (
            PROJECT_ROOT
            / relative_path
        )

        assert (
            path.is_file()
        ), (
            f"Missing release file: "
            f"{relative_path}"
        )

    run_all = (
        PROJECT_ROOT
        / "tests"
        / "run_all.py"
    )

    source = run_all.read_text(
        encoding="utf-8",
    )

    required_entries = (
        "tests.test_release_gate",
        "tests.test_repository_audit",
        "tests.test_e2e_production_flow",
        "tests.test_full_pipeline_e2e",
        "tests.test_full_system_validation",
        "tests.test_final_release",
    )

    for entry in required_entries:

        assert (
            f'"{entry}"'
            in source
        ), (
            f"Missing from run_all.py: "
            f"{entry}"
        )

    assert (
        "ALL TESTS PASSED"
        in source
    )

    assert (
        "Executed : {passed}"
        in source
    )

    result = git(
        "branch",
        "--show-current",
    )

    assert (
        result.returncode == 0
    ), result.stderr

    assert (
        result.stdout.strip()
        == "feature/log-001"
    ), (
        "Unexpected release branch: "
        + result.stdout.strip()
    )

    result = git(
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{u}",
    )

    assert (
        result.returncode == 0
    ), result.stderr

    assert (
        result.stdout.strip()
        == "origin/feature/log-001"
    ), (
        "Unexpected upstream: "
        + result.stdout.strip()
    )

    result = git(
        "rev-list",
        "--left-right",
        "--count",
        "HEAD...@{u}",
    )

    assert (
        result.returncode == 0
    ), result.stderr

    counts = (
        result.stdout
        .strip()
        .split()
    )

    assert (
        counts == ["0", "0"]
    ), (
        "Branch is not synchronized "
        "with origin: "
        + result.stdout.strip()
    )

    result = git(
        "log",
        "-1",
        "--format=%H",
    )

    assert (
        result.returncode == 0
    ), result.stderr

    head = result.stdout.strip()

    assert head

    print(
        "PASS : release files exist"
    )

    print(
        "PASS : final regression runner is registered"
    )

    print(
        "PASS : production E2E tests are registered"
    )

    print(
        "PASS : release branch is correct"
    )

    print(
        "PASS : upstream is correct"
    )

    print(
        "PASS : branch is synchronized"
    )

    print(
        "PASS : HEAD is valid"
    )

    print()

    print(
        f"RELEASE HEAD : {head}"
    )

    print()

    print("=" * 60)

    print(
        "FINAL RELEASE TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()