class EventBus:

    def __init__(self):

        self._listeners = {}

    def subscribe(
        self,
        event,
        callback,
    ):

        self._listeners.setdefault(
            event,
            [],
        ).append(callback)

    def emit(
        self,
        event,
        *args,
        **kwargs,
    ):

        for callback in self._listeners.get(
            event,
            [],
        ):
            callback(
                *args,
                **kwargs,
            )