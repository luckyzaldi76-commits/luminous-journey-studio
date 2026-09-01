import tempfile
from pathlib import Path

from services.production_orchestrator import (
    ProductionOrchestrator,
)


class FakeGospelInput:

    def normalize(
        self,
        gospel,
    ):

        gospel = gospel.strip()

        if not gospel:

            raise ValueError(
                "Gospel cannot be empty."
            )

        return gospel


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
            "output_dir": str(
                output_dir
            ),
            "script": (
                f"Script {language}"
            ),
        }


class FailingProductionPipeline:

    def __init__(
        self,
        failing_languages=None,
    ):

        self.failing_languages = set(
            failing_languages or ()
        )

    def generate(
        self,
        gospel,
        language,
        audience,
        output_dir,
        workflow_name,
    ):

        if language in self.failing_languages:

            raise RuntimeError(
                f"Generation failed: {language}"
            )

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
            "output_dir": str(
                output_dir
            ),
            "script": (
                f"Script {language}"
            ),
        }


class FakeMultilingualPipeline:

    def __init__(
        self,
        production_pipeline=None,
    ):

        self.pipeline = (
            production_pipeline
            or FakeProductionPipeline()
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

        supported = {
            "IND",
            "ENG",
            "ESP",
            "ZHT",
            "ZHS",
            "PINYIN",
        }

        for language in languages:

            language = (
                language
                .strip()
                .upper()
            )

            if language not in supported:

                raise ValueError(
                    f"Unsupported language: {language}"
                )

            if language not in result:

                result.append(language)

        if not result:

            raise ValueError(
                "At least one language is required."
            )

        return result


class FakeAssetPipeline:

    def export(
        self,
        result,
        output_dir,
    ):

        output_dir = Path(
            output_dir
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return {
            "output_dir": str(
                output_dir
            ),
            "exported": True,
        }


def test_successful_batch():

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)

        orchestrator = (
            ProductionOrchestrator(
                gospel_input=(
                    FakeGospelInput()
                ),
                multilingual_pipeline=(
                    FakeMultilingualPipeline()
                ),
                asset_pipeline=(
                    FakeAssetPipeline()
                ),
            )
        )

        result = orchestrator.run(
            gospel="  Lukas 5:33-39  ",
            languages=(
                "IND",
                "ENG",
                "ESP",
            ),
            audience="adult",
            output_dir=output_dir,
            workflow_name="Daily Gospel",
        )

        assert result["success"] is True

        assert result["gospel"] == (
            "Lukas 5:33-39"
        )

        assert result["languages"] == [
            "IND",
            "ENG",
            "ESP",
        ]

        assert result["total_jobs"] == 3
        assert result["completed_jobs"] == 3
        assert result["failed_jobs"] == 0

        assert len(
            result["jobs"]
        ) == 3

        assert all(
            job["status"] == "completed"
            for job in result["jobs"]
        )

        assert (
            output_dir / "IND"
        ).exists()

        assert (
            output_dir / "ENG"
        ).exists()

        assert (
            output_dir / "ESP"
        ).exists()


def test_prepare_creates_queued_jobs():

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)

        orchestrator = (
            ProductionOrchestrator(
                gospel_input=(
                    FakeGospelInput()
                ),
                multilingual_pipeline=(
                    FakeMultilingualPipeline()
                ),
                asset_pipeline=(
                    FakeAssetPipeline()
                ),
            )
        )

        jobs = orchestrator.prepare(
            gospel="Yohanes 20:24-29",
            languages=("IND", "ENG"),
            audience="adult",
            output_dir=output_dir,
        )

        assert len(jobs) == 2

        assert all(
            job.status == "queued"
            for job in jobs
        )


def test_partial_failure_continues_batch():

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)

        pipeline = (
            FailingProductionPipeline(
                failing_languages={"ENG"}
            )
        )

        orchestrator = (
            ProductionOrchestrator(
                gospel_input=(
                    FakeGospelInput()
                ),
                multilingual_pipeline=(
                    FakeMultilingualPipeline(
                        pipeline
                    )
                ),
                asset_pipeline=(
                    FakeAssetPipeline()
                ),
            )
        )

        result = orchestrator.run(
            gospel="Lukas 5:33-39",
            languages=(
                "IND",
                "ENG",
                "ESP",
            ),
            audience="adult",
            output_dir=output_dir,
            workflow_name="Daily Gospel",
        )

        assert result["success"] is False

        assert result["total_jobs"] == 3

        assert result["completed_jobs"] == 2

        assert result["failed_jobs"] == 1

        assert len(
            result["jobs"]
        ) == 3

        statuses = {
            job["result"]["language"]: job["status"]
            for job in result["jobs"]
            if job["result"]
        }

        assert statuses["IND"] == "completed"
        assert statuses["ESP"] == "completed"

        failed_jobs = [
            job
            for job in result["jobs"]
            if job["status"] == "failed"
        ]

        assert len(failed_jobs) == 1

        assert (
            failed_jobs[0]["error"]
            == "Generation failed: ENG"
        )

        assert (
            output_dir / "IND"
        ).exists()

        assert (
            output_dir / "ESP"
        ).exists()

        assert not (
            output_dir / "ENG" / "script.txt"
        ).exists()



def test_progress_is_returned():

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)

        orchestrator = ProductionOrchestrator(
            gospel_input=FakeGospelInput(),
            multilingual_pipeline=FakeMultilingualPipeline(),
            asset_pipeline=FakeAssetPipeline(),
        )

        result = orchestrator.run(
            gospel="Lukas 5:33-39",
            languages=(
                "IND",
                "ENG",
                "ESP",
            ),
            audience="adult",
            output_dir=output_dir,
            workflow_name="Daily Gospel",
        )

        assert "progress" in result

        progress = result["progress"]

        assert progress["total"] == 3
        assert progress["queued"] == 0
        assert progress["running"] == 0
        assert progress["completed"] == 3
        assert progress["failed"] == 0
        assert progress["remaining"] == 0
        assert progress["percentage"] == 100.0
        assert progress["finished"] is True
        assert progress["state"] == "completed"

def main():

    test_successful_batch()

    test_prepare_creates_queued_jobs()

    test_partial_failure_continues_batch()

    test_progress_is_returned()

    print("=" * 60)
    print(
        "PRODUCTION ORCHESTRATOR TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":

    main()