from core.bible_repository import BibleRepository

repo = BibleRepository()

print("=" * 40)

print("Books :", repo.total_books())

print("Chapters :", repo.total_chapters())

print("=" * 40)

chapter = repo.get_chapter("MAT", 14)

print(chapter)