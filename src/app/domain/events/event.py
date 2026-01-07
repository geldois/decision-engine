class Event:
    # constructor
    def __init__(self, event_id: int, event_type: str, event_payload: dict, event_timestamp: int):
        # validations
        if event_id is None or type(event_id) is not int or event_id < 0:
            raise ValueError("Event id is required")
        if event_type is None or type(event_type) is not str or not event_type.strip():
            raise ValueError("Event type is required")
        if event_payload is None:
            raise ValueError("Event payload is required")
        if event_timestamp is None or type(event_timestamp) is not int or event_timestamp < 0:
            raise ValueError("Event timestamp is required")
        # atributions
        self.event_id = event_id
        self.event_type = event_type.strip()
        self.event_payload = event_payload
        self.event_timestamp = event_timestamp
