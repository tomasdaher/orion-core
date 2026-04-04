import logging

from core.pipeline_registry import PipelineRegistry


class PipelineExecutor:
    """
    Pipeline Executor for Orion.

    Responsible for loading pipelines from the registry
    and executing them through the CapabilityEngine.
    """

    def __init__(self, capability_engine):

        self.logger = logging.getLogger("Orion")

        self.pipeline_registry = PipelineRegistry()

        self.capability_engine = capability_engine

    # ------------------------------------------------
    # Execute pipeline by name
    # ------------------------------------------------
    def execute(self, pipeline_name, state=None):

        self.logger.info(f"🚀 Executing pipeline: {pipeline_name}")

        pipeline = self.pipeline_registry.load_pipeline(pipeline_name)

        if not pipeline:

            self.logger.warning(
                f"⚠️ Pipeline not found: {pipeline_name}"
            )

            return state

        steps = pipeline.get("steps", [])

        if state is None:
            state = {}

        for step in steps:

            if not step.startswith("run_capability:"):

                self.logger.warning(
                    f"⚠️ Unknown step format: {step}"
                )

                continue

            capability_name = step.split(":")[1]

            self.logger.info(
                f"⚙️ Executing capability via engine: {capability_name}"
            )

            state = self.capability_engine.execute(
                capability_name,
                state
            )

        self.logger.info("✅ Pipeline execution finished")

        return state