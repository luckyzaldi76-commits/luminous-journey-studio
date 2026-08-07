from pathlib import Path
import time

from engine.production_engine import ProductionEngine


def main():

    start = time.perf_counter()

    engine = ProductionEngine()

    print("=" * 60)
    print("LUMINOUS JOURNEY STUDIO")
    print("=" * 60)
    print()

    print("Stage 1...")

    stage1 = engine.stage1.generate(
        gospel="Matthew 14:13-21",
        language="English",
        audience="Adults",
    )

    print("✓ Stage 1 completed")
    print()

    print("Stage 2...")
    print("Stage 3...")
    print("Stage 4...")
    print()

    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=3) as executor:

        future2 = executor.submit(
            engine.stage2.generate,
            stage1,
        )

        future3 = executor.submit(
            engine.stage3.generate,
            stage1,
        )

        future4 = executor.submit(
            engine.stage4.generate,
            "Matthew 14:13-21",
            "English",
            "Adults",
        )

        stage2 = future2.result()
        print("✓ Stage 2 completed")

        stage3 = future3.result()
        print("✓ Stage 3 completed")

        stage4 = future4.result()
        print("✓ Stage 4 completed")

    print()
    print("Exporting...")
    print()

    markdown = "\n\n".join(
        [
            stage1,
            stage2,
            stage3,
            stage4,
        ]
    )

    data = engine.run(
        gospel="Matthew 14:13-21",
        language="English",
        audience="Adults",
        output_dir=Path("exports/final"),
    )

    print("Done.")
    print()

    print("=" * 60)
    print("PRODUCTION FINISHED")
    print("=" * 60)
    print()

    print(data)

    print()
    print("=" * 60)
    print(
        f"Elapsed : {time.perf_counter()-start:.2f} sec"
    )
    print("=" * 60)


if __name__ == "__main__":

    main()