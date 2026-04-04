from bootstrap import build_system

from events.event_bus import EventBus
from events.trigger_engine import TriggerEngine
from events.event_listener import EventListener

from execution.execution_queue import ExecutionQueue
from execution.worker import Worker


def main():

    print("🚀 Orion Event System Starting")

    orchestrator = build_system()

    # ---------------------------------
    # Execution Queue
    # ---------------------------------

    execution_queue = ExecutionQueue()

    # Crear workers
    workers = []

    for i in range(3):

        worker = Worker(execution_queue, orchestrator)

        worker.start()

        workers.append(worker)

    # ---------------------------------
    # Event System
    # ---------------------------------

    event_bus = EventBus()

    trigger_engine = TriggerEngine(execution_queue)

    event_bus.subscribe(trigger_engine.handle_event)

    listener = EventListener(event_bus)

    listener.start()


if __name__ == "__main__":

    main()