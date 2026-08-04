from core.excel_reader import get_reading
from core.json_writer import save_json
from services.prompt_builder import build_prompt
from core.text_writer import save_prompt

print("=" * 50)
print("LUMINOUS JOURNEY STUDIO")
print("=" * 50)

tanggal = input("Masukkan tanggal (YYYY-MM-DD): ")

reading = get_reading(tanggal)

if reading:
    print()
    print("Tanggal   :", reading.date)
    print("Bacaan I  :", reading.reading1)
    print("Bacaan II :", reading.reading2)
    print("Injil     :", reading.gospel)

    file = save_json(reading)

    prompt = build_prompt(reading)

    txt = save_prompt(
        prompt,
        reading.date.replace("-", "") + "_PROMPT.txt"
    )

    print()
    print("Prompt berhasil dibuat")
    print(txt)

    print()
    print("JSON berhasil dibuat")
    print(file)

else:
    print("❌ Tanggal tidak ditemukan.")