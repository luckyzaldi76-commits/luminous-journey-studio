import time


class ProgressService:

    def __init__(self):

        self.total_start = time.perf_counter()

        self.stage_start = None

        self.current_stage = ""

    def header(
        self,
        version: str = "1.0",
    ):

        print()
        print("=" * 60)
        print(f"LUMINOUS JOURNEY STUDIO v{version}")
        print("=" * 60)
        print()

    def workflow(
        self,
        name: str,
    ):

        print(f"Workflow : {name}")
        print()

    def stage_starting(
        self,
        title: str,
    ):

        self.current_stage = title

        self.stage_start = time.perf_counter()

        print(f"▶ {title}...")

    def provider(
        self,
        provider: str,
    ):

        print(f"  Provider : {provider}")

    def stage_completed(
        self,
    ):

        elapsed = (
            time.perf_counter()
            - self.stage_start
        )

        print(
            f"✓ {self.current_stage} "
            f"({elapsed:.2f} s)"
        )

        print()

    def exporting(
        self,
    ):

        print("-" * 60)

        print("▶ Exporting files...")

        print()

    def exported(
        self,
        filename: str,
    ):

        print(f"✓ {filename}")

    def footer(
        self,
        provider: str,
        output_dir: str,
    ):

        total = (
            time.perf_counter()
            - self.total_start
        )

        print()

        print("-" * 60)

        print(f"AI Provider   : {provider}")

        print(f"Output Folder : {output_dir}")

        print(f"Total Time    : {total:.2f} s")

        print()

        print("=" * 60)

        print("Production completed successfully.")

        print("=" * 60)