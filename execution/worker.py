import threading


class Worker(threading.Thread):

    def __init__(self, execution_queue, orchestrator):

        super().__init__()

        self.execution_queue = execution_queue
        self.orchestrator = orchestrator

        self.daemon = True

    def run(self):

        print(f"🧵 Worker {self.name} started")

        while True:

            state = self.execution_queue.dequeue()

            try:

                print("⚙️ Worker executing Orion task")

                # 🔥 CAPTURAR RESULTADO
                result_state = self.orchestrator.run(state)

                # 🔍 DEBUG CLAVE
                if result_state:

                    plan = result_state.get("execution_plan")

                    if plan:
                        print(f"📋 Execution plan detected: {plan}")
                    else:
                        print("⚠️ No execution_plan in final state")

                    status = result_state.get("execution_status")
                    print(f"📊 Execution status: {status}")

            except Exception as e:

                print(f"❌ Worker execution error: {e}")

            finally:

                self.execution_queue.task_done()