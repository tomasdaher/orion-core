import logging
import time


class CognitiveLoop:

    """
    Orion Cognitive Loop

    Responsible for continuous autonomous execution.

    Observe
    Plan
    Act
    Reflect
    Learn
    """

    def __init__(self, orchestrator, max_cycles=5):

        self.orchestrator = orchestrator
        self.max_cycles = max_cycles
        self.logger = logging.getLogger("Orion.CognitiveLoop")

    # ------------------------------------------------

    def run(self, initial_state):

        state = initial_state

        self.logger.info("🧠 Starting Cognitive Loop")

        for cycle in range(self.max_cycles):

            self.logger.info(f"🔁 Cognitive cycle {cycle+1}")

            try:

                state = self.orchestrator.handle_request(
                    state.get("objective"),
                    state
                )

                if state.get("execution_status") != "SUCCESS":

                    self.logger.warning(
                        f"⚠️ Cycle failed: {state.get('execution_status')}"
                    )

                # reflection signal
                insights = state.get("reflection_insights")

                if insights:
                    self.logger.info(
                        f"🧠 Reflection insights detected"
                    )

                # optional stop condition
                if state.get("goal_completed"):

                    self.logger.info("🎯 Goal completed")
                    break

                time.sleep(0.5)

            except Exception as e:

                self.logger.error(
                    f"❌ Cognitive loop error: {str(e)}"
                )

        self.logger.info("🧠 Cognitive Loop finished")

        return state