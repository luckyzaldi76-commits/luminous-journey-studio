from pathlib import Path

from config import APP_DIR


class OutputService:

    def create(self, production_date):

        output_dir = (
            APP_DIR
            / "OUTPUTS"
            / production_date.replace("-", "")
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        print()
        print("=" * 60)
        print("OUTPUT SERVICE")
        print("=" * 60)
        print(f"Output Folder : {output_dir}")

        return output_dir


output_service = OutputService()