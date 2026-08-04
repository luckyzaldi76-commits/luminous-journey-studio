from services.ai_generator import generate_content
from core.json_parser import parse_ai_response

prompt = """
Return ONLY valid JSON.

{
    "theme":"",
    "reflection":""
}

Theme:
Jesus feeds the five thousand.
"""

print("Menghubungi AI...")

hasil = generate_content(prompt)

print("\nRAW RESPONSE")
print("=" * 60)
print(hasil)

data = parse_ai_response(hasil)

print("\nHASIL PARSER")
print("=" * 60)

if data:

    print("Theme")
    print(data["theme"])

    print()

    print("Reflection")
    print(data["reflection"])

else:

    print("Parser gagal.")