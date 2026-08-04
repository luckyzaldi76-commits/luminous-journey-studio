from core.bible_repository import BibleRepository

repo = BibleRepository()

print("=" * 40)

print("People :", repo.total_people())

print("=" * 40)

print(repo.get_person("JESUS"))