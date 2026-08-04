from core.bible_repository import BibleRepository

repo = BibleRepository()

print("="*40)

print("Books :", repo.total_books())

print("Chapters :", repo.total_chapters())

print("Verses :", repo.total_verses())

print("="*40)

print(repo.get_verse("MAT",14,22))