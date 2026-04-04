import logging


class ExecutionHistoryCollector:
    """
    Collects and stores execution pipelines from Orion runs.
    These pipelines are later used for capability learning.
    """

    def __init__(self, max_history=100):

        self.logger = logging.getLogger("Orion")

        # maximum stored executions
        self.max_history = max_history

        # internal history storage
        self.execution_history = []

    # ------------------------------------------------
    # Record execution pipeline
    # ------------------------------------------------
    def record_execution(self, pipeline):

        """
        pipeline example:

        ["planner_agent", "executor_agent", "validator_agent"]
        """

        if not pipeline:
            return

        try:

            normalized = self._normalize_pipeline(pipeline)

            self.execution_history.append(normalized)

            # limit memory size
            if len(self.execution_history) > self.max_history:
                self.execution_history.pop(0)

            self.logger.info(
                f"📜 Execution pipeline recorded: {normalized}"
            )

        except Exception as e:

            self.logger.warning(
                f"⚠️ Failed to record execution pipeline: {e}"
            )

    # ------------------------------------------------
    # Retrieve execution history
    # ------------------------------------------------
    def get_history(self):

        return list(self.execution_history)

    # ------------------------------------------------
    # Clear execution history
    # ------------------------------------------------
    def clear_history(self):

        self.execution_history = []

        self.logger.info("🧹 Execution history cleared")

    # ------------------------------------------------
    # Normalize pipeline names
    # ------------------------------------------------
    def _normalize_pipeline(self, pipeline):

        normalized = []

        for step in pipeline:

            if isinstance(step, str):

                name = step.lower()

            else:

                name = step.__class__.__name__.lower()

            normalized.append(name)

        return normalized