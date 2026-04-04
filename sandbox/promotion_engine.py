import shutil
import logging
from pathlib import Path


class CapabilityPromotionEngine:

    def __init__(self):

        self.logger = logging.getLogger("Orion")

        self.plugins_path = Path("plugins")
        self.plugins_path.mkdir(exist_ok=True)

    def promote(self, experiment_result):

        validation = experiment_result.get("validation", {})

        if not validation.get("approved"):

            self.logger.info("❌ Capability not approved, skipping promotion")
            return False

        source_file = Path(experiment_result["capability_file"])

        if not source_file.exists():

            self.logger.error("❌ Capability file not found")
            return False

        destination = self.plugins_path / source_file.name

        # 🔧 FIX: evitar copiar si ya está en plugins
        if source_file.resolve() == destination.resolve():

            self.logger.info("ℹ️ Capability already in plugins folder")
            return True

        try:

            shutil.copy(source_file, destination)

            self.logger.info(
                f"🚀 Capability promoted to production: {destination}"
            )

            return True

        except Exception as e:

            self.logger.error(f"Promotion failed: {e}")

            return False