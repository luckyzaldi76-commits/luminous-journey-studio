import tempfile
from pathlib import Path

from ljcli.main import main


ASSETS = (
    "script.txt",
    "response.md",
    "image_prompts.md",
    "seo.json",
    "metadata.json",
)


def main_test():

    with tempfile.TemporaryDirectory() as tmp:

        output_dir = Path(tmp)

        result = main(
            [
                "batch",
                "--gospel",
                "Lukas 5:33-39",
                "--languages",
                "IND,ENG",
                "--audience",
                "Catholic adults",
                "--output-dir",
                str(output_dir),
                "--workflow",
                "Daily Gospel",
            ]
        )

        assert result == 0

        assert (
            output_dir / "IND"
        ).exists()

        assert (
            output_dir / "ENG"
        ).exists()

        for language in (
            "IND",
            "ENG",
        ):

            language_dir = (
                output_dir / language
            )

            for name in ASSETS:

                assert (
                    language_dir / name
                ).exists(), (
                    f"Missing asset: "
                    f"{language}/{name}"
                )


if __name__ == "__main__":

    main_test()

    print("=" * 60)
    print(
        "CLI BATCH EXECUTION TEST PASSED"
    )
    print("=" * 60)
