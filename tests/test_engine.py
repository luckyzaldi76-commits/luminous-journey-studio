from pathlib import Path

from engine.production_engine import ProductionEngine


engine = ProductionEngine()

result = engine.run(
    gospel="Matthew 14:13-21",
    language="English",
    audience="Adults",
    output_dir=Path("exports/final"),
)

print(result)