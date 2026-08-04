from services.ai_generator import generate_content
import json

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

print("\nJSON TEST")
print("=" * 60)

try:

    data = json.loads(hasil)

    print("VALID JSON")
    print(data)

except Exception as e:

    print("BUKAN JSON")
    print(e)