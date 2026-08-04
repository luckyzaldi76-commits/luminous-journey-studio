from services.ai_generator import generate_content
from core.json_parser import parse_ai_response

prompt = """
Return ONLY valid JSON.

{
    "theme":"",
    "reflection":""
}

Gospel:
Matius 14:22-36
"""

print("=" * 60)
print("PROMPT")
print("=" * 60)
print(prompt)

print()
print("=" * 60)
print("AI RESPONSE")
print("=" * 60)

hasil = generate_content(prompt)

print()
print("HASIL AI")
print("=" * 60)
print(hasil)

print()
print("HASIL PARSER")
print("=" * 60)

data = parse_ai_response(hasil)

print("Theme      :", data["theme"])
print()
print("Reflection :")
print(data["reflection"])