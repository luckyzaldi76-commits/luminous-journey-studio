from pathlib import Path

from engine.production_engine import ProductionEngine


engine = ProductionEngine()

result = engine.run(
    Path("02_MASTER_PROMPT/master_prompt.md"),
    Path("exports/from_file"),
)

print(result)