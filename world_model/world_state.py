import time


class WorldState:

    def __init__(self):

        self.timestamp = time.time()
        self.entities = []
        self.events = []

    def snapshot(self, entities):

        self.timestamp = time.time()

        self.entities = [
            e.to_dict() for e in entities
        ]

    def record_event(self, event):

        self.events.append(event)

    def get_state(self):

        return {
            "timestamp": self.timestamp,
            "entities": self.entities,
            "events": self.events
        }