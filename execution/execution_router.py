import logging

from capabilities.registry import CapabilityRegistry
from tools.registry import ToolRegistry


class ExecutionRouter:

    def __init__(self):

        self.capability_registry = CapabilityRegistry()
        self.tool_registry = ToolRegistry()

        logging.info("ExecutionRouter initialized")

    # ------------------------------------------------

    def execute_plan(self, execution_plan: dict, state: dict):

        if not execution_plan:
            logging.warning("No execution plan found")
            return state

        steps = execution_plan.get("steps", [])

        if not steps:
            logging.warning("Execution plan has no steps")
            return state

        logging.info(f"Executing plan with {len(steps)} steps")

        for step in steps:

            state = self.execute_step(step, state)

        return state

    # ------------------------------------------------

    def execute_step(self, step: str, state: dict):

        logging.info(f"Executing step: {step}")

        # ------------------------------------------------
        # CAPABILITY EXECUTION
        # ------------------------------------------------

        if step.startswith("run_capability:"):

            capability_name = step.split(":")[1]

            capability = self.capability_registry.get_capability(
                capability_name
            )

            if not capability:

                logging.warning(
                    f"Capability not found: {capability_name}"
                )

                return state

            logging.info(
                f"Running capability: {capability_name}"
            )

            return capability.execute(state)

        # ------------------------------------------------
        # TOOL EXECUTION
        # ------------------------------------------------

        tool = self.tool_registry.get_tool(step)

        if tool:

            logging.info(f"Running tool: {step}")

            return tool.execute(state)

        # ------------------------------------------------
        # SKILL EXECUTION
        # ------------------------------------------------

        skill_handler = self.try_skill_execution(step, state)

        if skill_handler:

            return skill_handler

        logging.warning(f"Unknown step: {step}")

        return state

    # ------------------------------------------------

    def try_skill_execution(self, step: str, state: dict):

        import importlib

        skill_map = {
            "acquire_lead": ("skills.lead_engine.lead_source", "acquire_lead"),
            "capture_lead": ("skills.lead_engine.lead_capture", "capture_lead"),
            "clean_data": ("skills.lead_engine.lead_cleaner", "clean_lead_data"),
            "classify_lead": ("skills.lead_engine.lead_classifier", "classify_lead"),
            "score_lead": ("skills.lead_engine.lead_scorer", "score_lead"),
            "store_lead": ("skills.lead_engine.lead_storage", "store_lead"),
            "notify_sales": ("skills.lead_engine.lead_notifier", "notify_sales"),
        }

        if step not in skill_map:
            return None

        module_path, function_name = skill_map[step]

        try:

            module = importlib.import_module(module_path)

            skill_function = getattr(module, function_name, None)

            if not skill_function:

                logging.warning(
                    f"Skill function not found: {function_name}"
                )

                return state

            return skill_function(state)

        except Exception as e:

            logging.error(f"Skill execution error: {e}")

            return state