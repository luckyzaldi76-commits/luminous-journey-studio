from core.json_parser import parse_ai_response
from builders.seo_builder import builder

with open(
    "04_JSON/20260803_response.txt",
    encoding="utf-8"
) as f:

    text = f.read()

data = parse_ai_response(text)

builder.build(
    data,
    "sample.json"
)