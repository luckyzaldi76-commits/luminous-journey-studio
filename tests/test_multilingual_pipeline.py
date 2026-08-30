import tempfile
from pathlib import Path

from services.multilingual_pipeline import MultilingualGenerationPipeline


def main():

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)
        pipeline = MultilingualGenerationPipeline()

        results = pipeline.generate(
            gospel="Matius 24:42-51",
            languages=("ID", "EN"),
            audience="adult",
            output_dir=output_dir,
            workflow_name="Daily Gospel",
        )

        assert set(results) == {"ID", "EN"}
        assert results["ID"]["language"] == "ID"
        assert results["EN"]["language"] == "EN"
        assert results["ID"]["gospel"] == "Matius 24:42-51"
        assert results["EN"]["gospel"] == "Matius 24:42-51"
        assert (output_dir / "ID").exists()
        assert (output_dir / "EN").exists()

    print("=" * 60)
    print("MULTILINGUAL PIPELINE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
