import tempfile
from pathlib import Path

from ljcli.main import main


def main_test():

    with tempfile.TemporaryDirectory() as tmp:

        output_dir = Path(tmp)

        result = main(
            [
                "generate",
                "--gospel",
                "Lukas 5:33-39",
                "--language",
                "IND",
                "--audience",
                "Catholic adults",
                "--output-dir",
                str(output_dir),
            ]
        )

        assert result == 0

        assert (output_dir / "script.txt").exists()
        assert (output_dir / "response.md").exists()
        assert (output_dir / "image_prompts.md").exists()
        assert (output_dir / "seo.json").exists()
        assert (output_dir / "metadata.json").exists()


if __name__ == "__main__":

    main_test()

    print("=" * 60)
    print("CLI PRODUCTION GENERATION TEST PASSED")
    print("=" * 60)
