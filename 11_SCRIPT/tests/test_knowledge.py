from core.knowledge_loader import KnowledgeLoader

loader = KnowledgeLoader()

books = loader.load_books()

print("=" * 40)

for book in books.values():
    print(book["id"], "-", book["name"])

print("=" * 40)
print("Total :", len(books))