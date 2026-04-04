from agents.base_agent import BaseAgent
from core.execution_request import Objective

from workflows.workflow_registry import WorkflowRegistry
from workflows.workflow_engine import WorkflowEngine

from sandbox.experiment_manager import ExperimentManager
from core.capability_registry import CapabilityRegistry


class WorkflowAgent(BaseAgent):

    name = "Workflow_Agent"
    objective = Objective.PROCESS
    priority = 1  # 🔥 PRIMERO EN EJECUTARSE

    def __init__(self):

        super().__init__()

        self.workflow_registry = WorkflowRegistry()
        self.workflow_engine = WorkflowEngine(self.workflow_registry)

        self.capability_registry = CapabilityRegistry()
        self.experiment_manager = ExperimentManager(
            capability_registry=self.capability_registry
        )

        self._load_default_workflows()

    # ---------------------------------
    def _load_default_workflows(self):

        # 🔥 WORKFLOW PRINCIPAL ACTUALIZADO
        self.workflow_registry.register(
            "customer_onboarding",
            {
                "trigger": "new_customer",
                "actions": [
                    "send_webhook",
                    "create_user",
                    "segment_user"  # 🔥 NUEVA CAPABILITY
                ]
            }
        )

        self.workflow_registry.register(
            "order_processing",
            {
                "trigger": "new_order",
                "actions": [
                    "create_invoice",
                    "notify_sales"
                ]
            }
        )

    # ---------------------------------
    def _map_action_to_capability(self, action: str) -> str:

        mapping = {
            "send_webhook": "webhook_sender",
            "create_user": "user_creator",
            "segment_user": "user_segmenter",  # 🔥 NUEVO MAPEO
            "create_invoice": "invoice_creator",
            "notify_sales": "sales_notifier",
        }

        return mapping.get(action, f"generic_{action}")

    # ---------------------------------
    def execute(self, state: dict):

        # 🔥 SI YA HAY PLAN → NO TOCAR
        if state.get("execution_plan"):
            return state

        input_data = state.get("data", {})

        workflow = self.workflow_engine.match_workflow(input_data)

        # ---------------------------------
        # NO WORKFLOW → EXPERIMENTAR
        # ---------------------------------
        if not workflow:

            print("🧪 No workflow found → triggering experiment")

            try:
                result = self.experiment_manager.run_experiment(
                    "test_capability.py"
                )
                state["experiment_result"] = result

            except Exception as e:
                print(f"❌ ExperimentManager failed: {e}")

            return state

        # ---------------------------------
        # WORKFLOW ENCONTRADO
        # ---------------------------------
        print(f"⚙️ Workflow matched: {workflow.get('trigger')}")

        actions = workflow.get("actions", [])

        steps = []

        for action in actions:

            capability = self._map_action_to_capability(action)

            # 🔥 FORMATO CORRECTO
            steps.append(f"run_capability:{capability}")

        # ---------------------------------
        if not steps:

            print("⚠️ No steps generated → fallback to experiment")
            return state

        # ---------------------------------
        # 🔥 CREACIÓN DE PLAN + LOCK
        # ---------------------------------
        state["execution_plan"] = {
            "steps": steps,
            "source": "workflow",
            "strategy_mode": "deterministic"
        }

        # 🔥 BLOQUEO CRÍTICO
        state["lock_execution_plan"] = True

        print(f"📋 Workflow plan created: {state['execution_plan']}")
        print("🛑 Execution plan LOCKED (protected from overrides)")

        return state