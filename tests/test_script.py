from core.json_parser import parse_ai_response
from builders.script_builder import builder

with open(
    "04_JSON/20260803_response.txt",
    encoding="utf-8"
) as f:

    text = f.read()

data = parse_ai_response(text)

print("=" * 60)
print("DATA")
print("=" * 60)
print(data)

builder.build(
    data,
    "sample.txt"
)