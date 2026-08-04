from core.json_loader import JsonLoader


class BibleRepository:

    def __init__(self):

        loader = JsonLoader()

        self.books = loader.load_folder("KNOWLEDGE/01_BOOKS")
        self.chapters = loader.load_folder("KNOWLEDGE/02_CHAPTERS")
        self.verses = loader.load_folder("KNOWLEDGE/03_VERSES")
        self.people = loader.load_folder("KNOWLEDGE/04_PEOPLE")
        self.places = loader.load_folder("KNOWLEDGE/05_PLACES")
        self.events = loader.load_folder("KNOWLEDGE/06_EVENTS")
        self.themes = loader.load_folder("KNOWLEDGE/07_THEMES")
        self.words = loader.load_folder("KNOWLEDGE/08_WORDS")
        self.parables = loader.load_folder("KNOWLEDGE/09_PARABLES")
        self.miracles = loader.load_folder("KNOWLEDGE/10_MIRACLES")
        self.prophecies = loader.load_folder("KNOWLEDGE/11_PROPHECIES")
        self.saints = loader.load_folder("KNOWLEDGE/12_SAINTS")
        self.catechism = loader.load_folder("KNOWLEDGE/13_CATECHISM")
        self.liturgy = loader.load_folder("KNOWLEDGE/14_LITURGY")

    def get_book(self, id):
        return self.books.get(id)

    def get_chapter(self, book, chapter):
        return self.chapters.get(f"{book}_{chapter:02d}")

    def get_verse(self, book, chapter, verse):
        return self.verses.get(f"{book}_{chapter:02d}_{verse:02d}")

    def get_person(self, id):
        return self.people.get(id)

    def get_place(self, id):
        return self.places.get(id)

    def get_event(self, id):
        return self.events.get(id)

    def get_theme(self, id):
        return self.themes.get(id)

    def get_word(self, id):
        return self.words.get(id)

    def get_parable(self, id):
        return self.parables.get(id)

    def get_miracle(self, id):
        return self.miracles.get(id)

    def get_prophecy(self, id):
        return self.prophecies.get(id)

    def get_saint(self, id):
        return self.saints.get(id)

    def get_catechism(self, id):
        return self.catechism.get(id)

    def get_liturgy(self, id):
        return self.liturgy.get(id)