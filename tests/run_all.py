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
    "tests.test_e2e_production_flow",
    "tests.test_full_pipeline_e2e",
    "tests.test_full_system_validation",
    "tests.test_final_release",
    "tests.test_workflow_registry",
    "tests.test_workflow_runtime_integration",
    "tests.test_production_content_pipeline",
)


def run(test: str):

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
        print(
            f"FAILED : {test}"
        )

        sys.exit(
            result.returncode
        )

    print()
    print(
        f"PASSED : {test}"
    )
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
    print(
        f"Executed : {passed}"
    )
    print()


if __name__ == "__main__":

    main()