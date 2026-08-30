import tempfile
from pathlib import Path

from services.asset_pipeline import AssetPipeline


def main():

    with tempfile.TemporaryDirectory() as source:
        with tempfile.TemporaryDirectory() as destination:

            source_dir = Path(source)
            destination_dir = Path(destination)

            for name in AssetPipeline.ASSET_FILES:
                (source_dir / name).write_text(
                    name,
                    encoding="utf-8",
                )

            pipeline = AssetPipeline()

            exported = pipeline.export(
                source_dir,
                destination_dir,
            )

            assert set(exported) == set(
                AssetPipeline.ASSET_FILES
            )

            for name in AssetPipeline.ASSET_FILES:

                target = destination_dir / name

                assert target.exists()
                assert target.read_text(
                    encoding="utf-8"
                ) == name

    print("=" * 60)
    print("ASSET PIPELINE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
