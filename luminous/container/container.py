class Container:

    def __init__(self):

        self._services = {}

    def register(
        self,
        cls,
        instance,
    ):

        self._services[cls] = instance

    def resolve(
        self,
        cls,
    ):

        try:
            return self._services[cls]
        except KeyError as e:
            raise RuntimeError(
                f"Service not registered: {cls.__name__}"
            ) from e

    def exists(
        self,
        cls,
    ):

        return cls in self._services

    def clear(
        self,
    ):

        self._services.clear()