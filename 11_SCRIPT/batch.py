from datetime import datetime, timedelta
import subprocess

print("=" * 50)
print("LUMINOUS JOURNEY BATCH MODE")
print("=" * 50)

start = input("Tanggal awal (YYYY-MM-DD): ")
end = input("Tanggal akhir (YYYY-MM-DD): ")

start_date = datetime.strptime(start, "%Y-%m-%d")
end_date = datetime.strptime(end, "%Y-%m-%d")

current = start_date

while current <= end_date:

    tanggal = current.strftime("%Y-%m-%d")

    print("\n================================")
    print("Produksi :", tanggal)
    print("================================")

    subprocess.run(
        ["python", "app.py"],
        input=tanggal + "\n",
        text=True
    )

    current += timedelta(days=1)

print("\n================================")
print("SEMUA PRODUKSI SELESAI")
print("================================")