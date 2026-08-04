from core.bible_repository import BibleRepository

repo = BibleRepository()

print("=" * 40)

print(repo.total_books())

print("=" * 40)

mat = repo.get_book("MAT")

print(mat)

print("=" * 40)