from pathlib import Path
import time

from engine.production_engine import ProductionEngine


def main():

    engine = ProductionEngine()

    start = time.perf_counter()

    result = engine.run(
        gospel="Matthew 14:13-21",
        language="English",
        audience="Adults",
        output_dir=Path("exports/final"),
    )

    elapsed = time.perf_counter() - start

    print("=" * 60)
    print("PRODUCTION FINISHED")
    print("=" * 60)
    print()

    print(result)

    print()
    print("=" * 60)
    print(f"Elapsed : {elapsed:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()