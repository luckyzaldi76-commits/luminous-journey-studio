from pathlib import Path
from typing import Dict

from engine.production_engine import ProductionEngine


class ProductionContentPipeline:

    def __init__(self, engine=None):
        self.engine = engine or ProductionEngine()

    def generate(self, gospel: str, language: str, audience: str, output_dir: Path, workflow_name: str = "Daily Gospel") -> Dict:
        if not gospel.strip():
            raise ValueError("Gospel cannot be empty.")
        if not language.strip():
            raise ValueError("Language cannot be empty.")
        if not audience.strip():
            raise ValueError("Audience cannot be empty.")
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        result = self.engine.run(gospel=gospel, language=language, audience=audience, output_dir=output_dir, workflow_name=workflow_name)
        if not isinstance(result, dict):
            raise TypeError("Production engine must return a dict.")
        result.setdefault("gospel", gospel)
        result.setdefault("language", language)
        result.setdefault("audience", audience)
        result.setdefault("workflow", workflow_name)
        result.setdefault("output_dir", str(output_dir))
        return result
