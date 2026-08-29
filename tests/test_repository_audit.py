import os
import subprocess
from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve().parent.parent
)


REQUIRED_FILES = (
    "config/settings.py",
    "services/provider_health.py",
    "services/ai_service.py",
    "services/__init__.py",
    "ljcli/main.py",
    "tests/run_all.py",
    "tests/test_release_gate.py",
    "tests/test_final_production_hardening.py",
)


REQUIRED_TESTS = (
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
    "tests.test_provider_health_cross_process",
    "tests.test_provider_health_expiry",
    "tests.test_provider_health_concurrency",
    "tests.test_provider_health_observability",
    "tests.test_cli_health",
    "tests.test_ai_service_health_integration",
    "tests.test_ai_service_health_routing",
    "tests.test_ai_service_stream_health_routing",
    "tests.test_final_reliability",
    "tests.test_production_config",
    "tests.test_environment_safety",
    "tests.test_configuration_failure_handling",
    "tests.test_startup_validation",
    "tests.test_secret_safety",
    "tests.test_production_startup_health",
    "tests.test_final_production_hardening",
    "tests.test_release_gate",
    "tests.test_repository_audit",
)


def run_git(
    args,
    env,
):

    return subprocess.run(
        [
            "git",
            *args,
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def main():

    env = os.environ.copy()

    for relative_path in REQUIRED_FILES:

        path = (
            PROJECT_ROOT
            / relative_path
        )

        assert (
            path.is_file()
        ), (
            f"Missing required file: "
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

    for test_name in REQUIRED_TESTS:

        assert (
            f'"{test_name}"'
            in source
        ), (
            f"Missing from run_all.py: "
            f"{test_name}"
        )

    assert (
        "ALL TESTS PASSED"
        in source
    )

    assert (
        "sys.exit"
        in source
    )

    result = run_git(
        [
            "branch",
            "--show-current",
        ],
        env,
    )

    assert (
        result.returncode == 0
    ), result.stderr

    assert (
        result.stdout.strip()
        == "feature/log-001"
    ), (
        "Unexpected branch: "
        + result.stdout.strip()
    )

    result = run_git(
        [
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{u}",
        ],
        env,
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

    print(
        "PASS : all required production files exist"
    )

    print(
        "PASS : all 32 regression tests are registered"
    )

    print(
        "PASS : test runner has failure propagation"
    )

    print(
        "PASS : feature branch is correct"
    )

    print(
        "PASS : upstream branch is correct"
    )

    print()

    print("=" * 60)

    print(
        "REPOSITORY AUDIT TEST PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()