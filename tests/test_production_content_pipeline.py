import tempfile
from pathlib import Path

from services.content_pipeline import (
    ProductionContentPipeline,
)


class FakeEngine:

    def run(
        self,
        gospel,
        language,
        audience,
        output_dir,
        workflow_name,
    ):

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return {
            "script": "test script",
            "image_prompts": "test prompts",
            "title": "test title",
            "seo": {},
            "hashtags": [],
            "metadata": {},
            "gospel": gospel,
            "language": language,
            "audience": audience,
            "workflow": workflow_name,
            "output_dir": str(
                output_dir
            ),
        }


def main():

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)

        pipeline = ProductionContentPipeline(
            engine=FakeEngine()
        )

        result = pipeline.generate(
            gospel="Lukas 5:33-39",
            language="IND",
            audience="adult",
            output_dir=output_dir,
        )

        assert result["gospel"] == (
            "Lukas 5:33-39"
        )

        assert result["language"] == "IND"
        assert result["audience"] == "adult"

        assert result["job_id"]
        assert result["job_status"] == (
            "completed"
        )

        job = pipeline.job_service.get(
            result["job_id"]
        )

        assert job.status == "completed"
        assert job.result == result

        assert output_dir.exists()

    print("=" * 60)
    print(
        "PRODUCTION CONTENT PIPELINE TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
