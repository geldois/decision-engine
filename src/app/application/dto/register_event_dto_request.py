class RegisterEventDtoRequest:
    __slots__ = ("event_type", "payload", "timestamp")

    def __init__(self, event_type: str, payload: dict, timestamp: int):
        self.event_type = event_type
        self.payload = payload
        self.timestamp = timestamp
