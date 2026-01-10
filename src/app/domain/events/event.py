class Event:
    # constructor
    def __init__(self, event_type: str, payload: dict, timestamp: int, event_id: int = None):
        # validations
        if event_type is None or not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("Event type is required.")
        if payload is None:
            raise ValueError("Event payload is required.")
        if timestamp is None or not isinstance(timestamp, int) or timestamp < 0:
            raise ValueError("Event timestamp is required.")
        if event_id is not None and (not isinstance(event_id, int) or event_id < 0):
            raise ValueError("Event id is invalid.")
        # atributions
        self.event_type = event_type.strip()
        self.payload = payload
        self.timestamp = timestamp
        self.event_id = event_id
