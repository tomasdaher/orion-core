import os
import logging
from datetime import datetime

from sandbox.experiment_manager import ExperimentManager


class CapabilityBuilder:

    def __init__(self, capability_engine, plugins_path="plugins", registry=None):

        self.logger = logging.getLogger("Orion")

        self.capability_engine = capability_engine
        self.plugins_path = plugins_path

        # 🔥 Sandbox como filtro real
        self.experiment_manager = ExperimentManager(
            capability_registry=registry
        )

        if not os.path.exists(self.plugins_path):
            os.makedirs(self.plugins_path)

    # ------------------------------------------------
    # Ensure capability exists
    # ------------------------------------------------
    def ensure_capability(self, capability_name):

        # ✅ Ya existe
        if self.capability_engine.has_capability(capability_name):
            return True

        self.logger.info(
            f"🧠 Capability missing → building via sandbox: {capability_name}"
        )

        try:

            # ------------------------------------------------
            # 1. Crear archivo
            # ------------------------------------------------
            filepath = self._create_capability(capability_name)

            if not filepath:
                raise Exception("Failed to create capability file")

            # ------------------------------------------------
            # 2. Ejecutar experimento (SANDBOX)
            # ------------------------------------------------
            result = self.experiment_manager.run_experiment(filepath)

            # ------------------------------------------------
            # 3. VALIDACIÓN REAL (SIN FALLBACK)
            # ------------------------------------------------
            if result and result.get("promoted"):

                self.logger.info(
                    f"🚀 Capability approved by sandbox: {capability_name}"
                )

                return True

            # ❌ RECHAZO TOTAL
            self.logger.error(
                f"❌ Sandbox rejected capability: {capability_name}"
            )

            return False

        except Exception as e:

            self.logger.error(
                f"❌ Capability build failed: {e}"
            )

            return False

    # ------------------------------------------------
    # Create capability file
    # ------------------------------------------------
    def _create_capability(self, capability_name):

        filename = f"{capability_name}.py"
        filepath = os.path.join(self.plugins_path, filename)

        if os.path.exists(filepath):

            self.logger.info(
                f"Capability file already exists: {filename}"
            )

            return filepath

        try:

            class_name = self._class_name(capability_name)
            code = self._generate_capability_code(class_name)

            with open(filepath, "w") as f:
                f.write(code)

            self.logger.info(
                f"📦 New capability created: {filename}"
            )

            return filepath

        except Exception as e:

            self.logger.error(
                f"Failed creating capability {capability_name}: {e}"
            )

            return None

    # ------------------------------------------------
    def _class_name(self, capability_name):

        parts = capability_name.split("_")
        return "".join(p.capitalize() for p in parts)

    # ------------------------------------------------
    def _generate_capability_code(self, class_name):

        timestamp = datetime.utcnow().isoformat()

        return f'''
"""
Auto-generated capability

Created by Orion
Timestamp: {timestamp}
"""


class {class_name}:

    def __init__(self):
        self.name = "{class_name}"

    def execute(self, state):

        data = state.get("data", {{}})

        result = {{
            "capability": self.name,
            "status": "executed",
            "data_received": data
        }}

        state["last_capability"] = self.name

        return result
'''.strip()