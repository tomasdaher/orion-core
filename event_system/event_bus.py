class EventBus:

    def __init__(self):

        self.queue = []

    def publish(self, event):

        print(f"📡 Event published: {event.type}")

        self.queue.append(event)

    def consume(self):

        if not self.queue:
            return None

        return self.queue.pop(0)

    def has_events(self):

        return len(self.queue) > 0