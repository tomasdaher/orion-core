import json
import logging
from datetime import datetime
from pathlib import Path

from sandbox.code_runner import SandboxCodeRunner
from sandbox.validation_engine import ValidationEngine
from sandbox.promotion_engine import CapabilityPromotionEngine


class ExperimentManager:

    def __init__(self, capability_registry=None):

        self.logger = logging.getLogger("Orion")

        self.runner = SandboxCodeRunner()
        self.validator = ValidationEngine()
        self.promoter = CapabilityPromotionEngine()

        # 🔗 conexión con registry
        self.registry = capability_registry

        self.experiments_path = Path("sandbox/experiments")
        self.experiments_path.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------
    # RUN EXPERIMENT
    # ------------------------------------------------
    def run_experiment(self, capability_file):

        self.logger.info(
            f"🧪 Running experiment for {capability_file}"
        )

        test_state = {
            "data": {
                "sample": "test_input"
            }
        }

        # ----------------------------------------
        # EXECUTION
        # ----------------------------------------
        try:

            execution = self.runner.run_capability(
                capability_file,
                test_state
            )

        except Exception as e:

            self.logger.error(
                f"❌ Execution failed: {e}"
            )

            execution = {
                "status": "error",
                "error": str(e)
            }

        # 🧪 DEBUG PROFUNDO
        self.logger.info(f"🧪 Execution result: {execution}")

        # ----------------------------------------
        # VALIDATION
        # ----------------------------------------
        try:

            validation = self.validator.validate(execution)

        except Exception as e:

            self.logger.error(
                f"❌ Validation crashed: {e}"
            )

            validation = {"valid": False, "error": str(e)}

        # 🧪 DEBUG PROFUNDO
        self.logger.info(f"🧪 Validation result: {validation}")

        # ----------------------------------------
        # STORE RESULT
        # ----------------------------------------
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "capability_file": capability_file,
            "execution": execution,
            "validation": validation
        }

        self._store_experiment(result)

        # ----------------------------------------
        # PROMOTION LOGIC (FIX CLAVE)
        # ----------------------------------------
        promoted = False

        try:

            is_valid = validation.get("approved") is True

            if is_valid:

                self.logger.info("✅ Validation passed → promoting capability")

                promoted = self.promoter.promote(result)

            else:

                self.logger.info("⚠️ Validation failed → not promoting")

        except Exception as e:

            self.logger.error(
                f"❌ Promotion failed: {e}"
            )

        result["promoted"] = promoted

        # ----------------------------------------
        # POST-PROMOTION
        # ----------------------------------------
        if promoted:

            self.logger.info("🚀 Capability promoted to production")

            if self.registry:

                try:
                    self.logger.info("♻️ Reloading capability registry...")

                    self.registry.reload()

                    self.logger.info("✅ Registry updated successfully")

                except Exception as e:

                    self.logger.warning(
                        f"⚠️ Registry reload failed: {e}"
                    )

        else:

            self.logger.info("⚠️ Capability not promoted")

        return result

    # ------------------------------------------------
    # STORE RESULT
    # ------------------------------------------------
    def _store_experiment(self, result):

        filename = f"experiment_{datetime.utcnow().timestamp()}.json"

        filepath = self.experiments_path / filename

        try:

            with open(filepath, "w") as f:
                json.dump(result, f, indent=2)

        except Exception as e:

            self.logger.warning(
                f"⚠️ Failed to store experiment: {e}"
            )