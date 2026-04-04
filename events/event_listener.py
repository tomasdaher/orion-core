import time
from events.event import Event


class EventListener:

    def __init__(self, event_bus, interval=10, max_events=5):

        self.event_bus = event_bus
        self.interval = interval
        self.max_events = max_events

    def start(self):

        print("👂 Event listener started")

        event_count = 0

        while event_count < self.max_events:

            event_count += 1

            event = Event(
                "new_customer",
                {
                    "trigger": "new_customer",
                    "name": f"Customer {event_count}",  # 🔥 FIX AQUÍ
                    "email": f"customer{event_count}@example.com"
                }
            )

            print(f"\n📡 Emitting event {event_count}/{self.max_events}")
            print(f"⚡ Event: {event.name}")

            self.event_bus.publish(event)

            time.sleep(self.interval)

        print("\n🛑 Event listener finished")