import logging


class LeadPipeline:

    name = "lead_engine_pipeline"

    def __init__(self):

        logging.info("LeadPipeline initialized (legacy compatibility mode)")

        # pipeline legacy (no longer used by Orion ExecutionRouter)
        self.steps = []

    def execute(self, state):

        logging.warning(
            "LeadPipeline is deprecated. Execution handled by ExecutionRouter."
        )

        return state