import tempfile
from pathlib import Path

from services.multilingual_pipeline import (
    MultilingualGenerationPipeline,
)


def main():

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)

        pipeline = (
            MultilingualGenerationPipeline()
        )

        results = pipeline.generate(
            gospel="Matius 24:42-51",
            languages=("IND", "ENG"),
            audience="adult",
            output_dir=output_dir,
            workflow_name="Daily Gospel",
        )

        assert set(results) == {
            "IND",
            "ENG",
        }

        assert (
            results["IND"]["language"]
            == "IND"
        )

        assert (
            results["ENG"]["language"]
            == "ENG"
        )

        assert (
            results["IND"]["gospel"]
            == "Matius 24:42-51"
        )

        assert (
            results["ENG"]["gospel"]
            == "Matius 24:42-51"
        )

        assert (
            output_dir / "IND"
        ).exists()

        assert (
            output_dir / "ENG"
        ).exists()

        duplicate_results = (
            pipeline.generate(
                gospel="Matius 24:42-51",
                languages=(
                    "IND",
                    "IND",
                    "ENG",
                ),
                audience="adult",
                output_dir=output_dir,
            )
        )

        assert set(
            duplicate_results
        ) == {
            "IND",
            "ENG",
        }

        try:

            pipeline.generate(
                gospel="Test",
                languages=("XXX",),
                audience="adult",
                output_dir=output_dir,
            )

            raise AssertionError(
                "Unsupported language should fail."
            )

        except ValueError as error:

            assert (
                "Unsupported language"
                in str(error)
            )

    print("=" * 60)
    print(
        "MULTILINGUAL BATCH PIPELINE TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":

    main()