import importlib.util
import logging
import time
from pathlib import Path


class SandboxCodeRunner:

    def __init__(self):

        self.logger = logging.getLogger("Orion")

    def run_capability(self, filepath, test_state):

        self.logger.info(f"🧪 Sandbox executing: {filepath}")

        try:

            start_time = time.time()

            spec = importlib.util.spec_from_file_location(
                "sandbox_module",
                filepath
            )

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            # encontrar clase
            capability_class = None

            for attr in dir(module):

                obj = getattr(module, attr)

                if isinstance(obj, type):
                    capability_class = obj
                    break

            if not capability_class:
                raise Exception("No capability class found")

            instance = capability_class()

            result = instance.execute(test_state)

            execution_time = time.time() - start_time

            return {
                "success": True,
                "execution_time": execution_time,
                "result": result
            }

        except Exception as e:

            self.logger.error(f"Sandbox execution failed: {e}")

            return {
                "success": False,
                "error": str(e)
            }