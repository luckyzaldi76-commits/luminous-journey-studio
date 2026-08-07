class Registry:

    def __init__(self):

        self._items = {}

    def register(
        self,
        name,
        item,
    ):

        self._items[name] = item

    def get(
        self,
        name,
    ):

        return self._items[name]

    def exists(
        self,
        name,
    ):

        return name in self._items

    def all(self):

        return self._items.copy()