class Event:

    def __init__(self, name, payload=None):

        self.name = name
        self.payload = payload or {}