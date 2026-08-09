from pathlib import Path

from engine.production_engine import ProductionEngine


def main():

    engine = ProductionEngine()

    data = engine.run(

        workflow_name="daily_gospel",

        gospel="Matthew 14:13-21",

        language="English",

        audience="Adults",

        output_dir=Path("exports"),

    )

    assert data["title"]

    assert data["script"]

    assert data["seo"]

    assert data["hashtags"]

    assert data["image_prompts"]

    assert data["metadata"]

    print()

    print("=" * 60)

    print("ENGINE TEST PASSED")

    print("=" * 60)


if __name__ == "__main__":

    main()