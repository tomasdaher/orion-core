from core.execution_request import Objective


class TriggerEngine:

    def __init__(self, execution_queue):

        self.execution_queue = execution_queue

    def handle_event(self, event):

        state = {
            "objective": Objective.PROCESS,
            "data": event.payload
        }

        print(f"⚡ Trigger received: {event.name}")

        self.execution_queue.enqueue(state)