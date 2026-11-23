class EventDispatcher:

    def __init__(self, event_bus, registry):

        self.event_bus = event_bus
        self.registry = registry

    def dispatch(self):

        while self.event_bus.has_events():

            event = self.event_bus.consume()

            handlers = self.registry.get_handlers(event.type)

            for handler in handlers:

                try:

                    print(f"⚡ Handling event: {event.type}")

                    handler(event.payload)

                except Exception as e:

                    print(f"❌ Event handler error: {e}")