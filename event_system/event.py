import uuid
import time


class Event:

    def __init__(self, event_type, payload=None):

        self.id = str(uuid.uuid4())
        self.type = event_type
        self.payload = payload or {}

        self.timestamp = time.time()

    def to_dict(self):

        return {
            "id": self.id,
            "type": self.type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }