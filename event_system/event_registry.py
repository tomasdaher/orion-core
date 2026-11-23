class EventRegistry:

    def __init__(self):

        self.handlers = {}

    def register(self, event_type, handler):

        if event_type not in self.handlers:
            self.handlers[event_type] = []

        self.handlers[event_type].append(handler)

    def get_handlers(self, event_type):

        return self.handlers.get(event_type, [])