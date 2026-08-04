import json

from core.section_parser import parser

with open(
    "04_JSON/Matius_13-54-58.json",
    encoding="utf-8"
) as f:
    data = json.load(f)

sections = parser.parse(data["content"])

print("=" * 60)

for key in sections:
    print(key)