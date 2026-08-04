from core.markdown_parser import parse_markdown

with open(
    "03_RESPONSE/20260731_response.txt",
    encoding="utf-8"
) as f:

    text = f.read()

data = parse_markdown(text)

print("=" * 60)

for key, value in data.items():

    print(key)

    print("-" * 40)

    print(value[:200])

    print()