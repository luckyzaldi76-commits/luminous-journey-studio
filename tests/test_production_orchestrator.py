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


def main():

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

    print("=" * 60)
    print(
        "PRODUCTION ORCHESTRATOR TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
