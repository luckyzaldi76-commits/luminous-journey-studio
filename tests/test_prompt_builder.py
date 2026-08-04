from pathlib import Path

from engine.production_engine import ProductionEngine


engine = ProductionEngine()

result = engine.run(
    Path("02_MASTER_PROMPT/template.md"),
    Path("exports/template"),
    gospel="Matthew 14:13-21",
    language="English",
    audience="Adults",
)

print(result)