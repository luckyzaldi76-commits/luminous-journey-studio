import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.prompt_reader import load_prompt

prompt = load_prompt()

print("=" * 60)
print("MASTER PROMPT")
print("=" * 60)

print(prompt[:1000])