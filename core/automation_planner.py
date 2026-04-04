import logging

from core.pipeline_registry import PipelineRegistry


class AutomationPlanner:
    """
    Automation Planner for Orion.

    Converts structured intents into executable
    automation pipelines and stores them
    for future reuse.
    """

    def __init__(self):

        self.logger = logging.getLogger("Orion")

        # Pipeline storage
        self.pipeline_registry = PipelineRegistry()

        # ------------------------------------------------
        # ACTION → CAPABILITY MAP (NEW)
        # ------------------------------------------------
        self.action_capability_map = {

            "capture": "lead_capture",
            "collect": "lead_capture",

            "clean": "lead_cleaner",
            "sanitize": "lead_cleaner",

            "classify": "lead_classifier",
            "score": "lead_classifier",
            "segment": "lead_classifier",

            "store": "lead_storage",
            "save": "lead_storage",
            "persist": "lead_storage",

            "notify": "lead_notifier",
            "alert": "lead_notifier",
            "inform": "lead_notifier"

        }

    # ------------------------------------------------
    # Main planner entrypoint
    # ------------------------------------------------
    def plan(self, intent):

        if not intent:
            self.logger.warning("⚠️ Empty intent received")
            return self.empty_plan()

        self.logger.info(f"🧠 AutomationPlanner received intent: {intent}")

        goal = intent.get("goal")

        if goal == "lead_generation":
            return self.build_lead_pipeline(intent)

        self.logger.warning(f"⚠️ Unknown automation goal: {goal}")

        return self.empty_plan()

    # ------------------------------------------------
    # Empty plan fallback
    # ------------------------------------------------
    def empty_plan(self):

        return {
            "steps": [],
            "source": "automation_planner",
            "strategy_mode": "generated"
        }

    # ------------------------------------------------
    # Lead automation pipeline
    # ------------------------------------------------
    def build_lead_pipeline(self, intent):

        self.logger.info("📋 Building lead generation pipeline")

        steps = []

        actions = intent.get("actions") or []
        conditions = intent.get("conditions") or []

        # Normalize actions
        actions = [a.lower() for a in actions]

        # ---------------------------------------------
        # Capture step
        # ---------------------------------------------
        self.logger.info("⚙️ Adding capture step")

        steps += self.add_capture_step()

        # ---------------------------------------------
        # Processing steps
        # ---------------------------------------------
        self.logger.info("⚙️ Adding processing steps")

        steps += self.add_processing_steps(actions)

        # ---------------------------------------------
        # Output steps
        # ---------------------------------------------
        self.logger.info("⚙️ Adding output steps")

        steps += self.add_output_steps(actions)

        # ---------------------------------------------
        # Dynamic steps (NEW)
        # ---------------------------------------------
        self.logger.info("⚙️ Checking dynamic actions")

        steps += self.add_dynamic_steps(actions, steps)

        execution_plan = {
            "steps": steps,
            "conditions": conditions,
            "source": "automation_planner",
            "strategy_mode": "generated"
        }

        self.logger.info(f"📋 Generated automation plan: {execution_plan}")

        # ---------------------------------------------
        # Save pipeline automatically
        # ---------------------------------------------
        self.save_generated_pipeline(intent, execution_plan)

        return execution_plan

    # ------------------------------------------------
    # Save generated pipeline
    # ------------------------------------------------
    def save_generated_pipeline(self, intent, execution_plan):

        goal = intent.get("goal", "automation")

        source = intent.get("source", "generic")

        pipeline_name = f"{goal}_{source}"

        try:

            self.logger.info(f"💾 Saving generated pipeline: {pipeline_name}")

            self.pipeline_registry.save_pipeline(
                pipeline_name,
                execution_plan
            )

        except Exception as e:

            self.logger.warning(
                f"⚠️ Failed saving pipeline: {e}"
            )

    # ------------------------------------------------
    # Capture lead source
    # ------------------------------------------------
    def add_capture_step(self):

        return ["run_capability:lead_capture"]

    # ------------------------------------------------
    # Data processing
    # ------------------------------------------------
    def add_processing_steps(self, actions):

        steps = []

        if "clean" in actions:
            steps.append("run_capability:lead_cleaner")

        if "classify" in actions:
            steps.append("run_capability:lead_classifier")

        return steps

    # ------------------------------------------------
    # Output actions
    # ------------------------------------------------
    def add_output_steps(self, actions):

        steps = []

        if "store" in actions:
            steps.append("run_capability:lead_storage")

        if "notify" in actions:
            steps.append("run_capability:lead_notifier")

        return steps

    # ------------------------------------------------
    # Dynamic action mapping (NEW)
    # ------------------------------------------------
    def add_dynamic_steps(self, actions, existing_steps):

        steps = []

        for action in actions:

            capability = self.action_capability_map.get(action)

            if not capability:
                continue

            step = f"run_capability:{capability}"

            if step not in existing_steps and step not in steps:

                self.logger.info(
                    f"⚙️ Adding dynamic capability step: {capability}"
                )

                steps.append(step)

        return steps