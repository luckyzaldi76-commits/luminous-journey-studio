import tempfile
from pathlib import Path

from services.content_pipeline import ProductionContentPipeline


def main():
    with tempfile.TemporaryDirectory() as temp:
        output_dir = Path(temp)
        pipeline = ProductionContentPipeline()
        result = pipeline.generate(gospel="Matius 24:42-51", language="ID", audience="adult", output_dir=output_dir, workflow_name="Daily Gospel")
        assert isinstance(result, dict)
        assert result["gospel"] == "Matius 24:42-51"
        assert result["language"] == "ID"
        assert result["audience"] == "adult"
        assert result["workflow"] == "Daily Gospel"
        assert result["output_dir"] == str(output_dir)
        assert list(output_dir.rglob("*"))
    print("=" * 60)
    print("PRODUCTION CONTENT PIPELINE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
