from queue import Queue


class ExecutionQueue:

    def __init__(self):

        self.queue = Queue()

    def enqueue(self, state):

        print("📥 Event added to execution queue")

        self.queue.put(state)

    def dequeue(self):

        return self.queue.get()

    def task_done(self):

        self.queue.task_done()