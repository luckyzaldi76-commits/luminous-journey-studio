import tempfile
from pathlib import Path

from services.multilingual_job_pipeline import (
    MultilingualJobPipeline,
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
            "output_dir": str(output_dir),
        }


class FakeMultilingualPipeline:

    LANGUAGES = (
        "IND",
        "ENG",
        "ESP",
        "ZHT",
        "ZHS",
        "PINYIN",
    )

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

            language = language.strip().upper()

            if language not in self.LANGUAGES:

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


def main():

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)

        pipeline = MultilingualJobPipeline(
            multilingual_pipeline=(
                FakeMultilingualPipeline()
            )
        )

        result = pipeline.run(
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

        assert result["gospel"] == (
            "Lukas 5:33-39"
        )

        assert result["audience"] == (
            "adult"
        )

        assert result["workflow"] == (
            "Daily Gospel"
        )

        assert result["languages"] == [
            "IND",
            "ENG",
            "ESP",
        ]

        assert result["success"] is True

        assert len(
            result["jobs"]
        ) == 3

        assert all(
            job["status"] == "completed"
            for job in result["jobs"]
        )

        assert {
            job["language"]
            for job in result["jobs"]
        } == {
            "IND",
            "ENG",
            "ESP",
        }

        assert (
            output_dir / "IND"
        ).exists()

        assert (
            output_dir / "ENG"
        ).exists()

        assert (
            output_dir / "ESP"
        ).exists()

        duplicate_result = pipeline.run(
            gospel="Lukas 5:33-39",
            languages=(
                "IND",
                "IND",
                "ENG",
            ),
            audience="adult",
            output_dir=output_dir,
        )

        assert duplicate_result[
            "languages"
        ] == [
            "IND",
            "ENG",
        ]

        assert len(
            duplicate_result["jobs"]
        ) == 2

    print("=" * 60)
    print(
        "MULTILINGUAL JOB PIPELINE TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
