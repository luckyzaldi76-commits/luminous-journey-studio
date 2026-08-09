class EventBus:

    def __init__(self):

        self._listeners = {}

    def subscribe(
        self,
        event: str,
        callback,
    ):

        self._listeners.setdefault(

            event,

            [],

        ).append(

            callback,

        )

    def unsubscribe(
        self,
        event: str,
        callback,
    ):

        listeners = self._listeners.get(
            event,
        )

        if listeners is None:

            return

        if callback in listeners:

            listeners.remove(
                callback,
            )

        if not listeners:

            self._listeners.pop(
                event,
                None,
            )

    def emit(
        self,
        event: str,
        *args,
        **kwargs,
    ):

        listeners = tuple(

            self._listeners.get(
                event,
                (),
            )

        )

        for callback in listeners:

            callback(

                *args,

                **kwargs,

            )

    def has(
        self,
        event: str,
    ) -> bool:

        return (

            event in self._listeners

            and

            bool(

                self._listeners[event]

            )

        )

    def clear(
        self,
    ):

        self._listeners.clear()

    def listeners(
        self,
        event: str,
    ) -> tuple:

        return tuple(

            self._listeners.get(
                event,
                (),
            )

        )

    def events(
        self,
    ) -> tuple:

        return tuple(

            sorted(

                self._listeners.keys()

            )

        )

    def __len__(
        self,
    ) -> int:

        return sum(

            len(listeners)

            for listeners in self._listeners.values()

        )