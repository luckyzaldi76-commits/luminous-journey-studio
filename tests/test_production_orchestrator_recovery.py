import tempfile
from pathlib import Path

from services.asset_pipeline import AssetPipeline
from services.job_queue import ProductionJobQueue
from services.job_service import JobService
from services.job_store import PersistentJobStore
from services.production_orchestrator import (
    ProductionOrchestrator,
)


class FakeProductionPipeline:

    def generate(
        self,
        gospel,
        language,
        audience,
        output_dir,
        workflow_name,
    ):

        output_dir = Path(
            output_dir
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return {
            "gospel": gospel,
            "language": language,
            "audience": audience,
            "workflow": workflow_name,
            "script": f"Recovered {language}",
        }


class FakeMultilingualPipeline:

    def __init__(self):

        self.pipeline = (
            FakeProductionPipeline()
        )

    def _normalize_languages(
        self,
        languages,
    ):

        if isinstance(
            languages,
            str,
        ):

            languages = (
                languages,
            )

        result = []

        for language in languages:

            language = (
                language
                .strip()
                .upper()
            )

            if language not in result:

                result.append(
                    language
                )

        if not result:

            raise ValueError(
                "At least one language is required."
            )

        return result


class FakeAssetPipeline:

    def export(
        self,
        source_dir,
        destination_dir,
    ):

        return []


def main():

    with tempfile.TemporaryDirectory() as temp:

        root = Path(
            temp
        )

        store_path = (
            root / "jobs.json"
        )

        store = PersistentJobStore(
            store_path
        )

        job_service = JobService(
            store=store
        )

        queue = ProductionJobQueue(
            job_service=job_service
        )

        orchestrator = ProductionOrchestrator(
            multilingual_pipeline=(
                FakeMultilingualPipeline()
            ),
            job_queue=queue,
            asset_pipeline=(
                FakeAssetPipeline()
            ),
        )

        job = queue.create()

        job.result = {
            "gospel": "Lukas 5:33-39",
            "language": "ENG",
            "audience": "adult",
            "workflow": "Daily Gospel",
            "output_dir": str(
                root / "ENG"
            ),
        }

        store.save(
            job
        )

        job_service.start(
            job.job_id
        )

        restarted_service = JobService(
            store=PersistentJobStore(
                store_path
            )
        )

        restarted_queue = ProductionJobQueue(
            job_service=restarted_service
        )

        restarted_orchestrator = (
            ProductionOrchestrator(
                multilingual_pipeline=(
                    FakeMultilingualPipeline()
                ),
                job_queue=restarted_queue,
                asset_pipeline=(
                    FakeAssetPipeline()
                ),
            )
        )

        result = (
            restarted_orchestrator.recover()
        )

        assert result["success"] is True

        assert result["total_jobs"] == 1

        assert result["recovered_jobs"] == 1

        assert result["completed_jobs"] == 1

        assert result["failed_jobs"] == 0

        assert result["progress"]["total"] == 1

        assert result["progress"]["completed"] == 1

        assert result["progress"]["failed"] == 0

        assert result["progress"]["remaining"] == 0

        assert result["progress"]["percentage"] == 100.0

        assert result["progress"]["finished"] is True

        assert result["progress"]["state"] == (
            "completed"
        )

        recovered_job = result["jobs"][0]

        assert recovered_job["job_id"] == (
            job.job_id
        )

        assert recovered_job["status"] == (
            "completed"
        )

        final_service = JobService(
            store=PersistentJobStore(
                store_path
            )
        )

        final_job = final_service.get(
            job.job_id
        )

        assert final_job.status == (
            "completed"
        )

        assert final_job.result["language"] == (
            "ENG"
        )

        assert final_job.result["content"][
            "script"
        ] == "Recovered ENG"


if __name__ == "__main__":

    main()

    print("=" * 60)
    print(
        "PRODUCTION ORCHESTRATOR RECOVERY TEST PASSED"
    )
    print("=" * 60)