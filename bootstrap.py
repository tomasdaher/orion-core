from core.orchestrator import Orchestrator
from core.rule_engine import Rule
from core.execution_request import Objective
from agents.task_agent import TaskAgent
from agents.decision_agent import DecisionAgent
from infrastructure.repositories.sqlite_execution_repository import SQLiteExecutionRepository


def build_system():
    # Infraestructura
    repository = SQLiteExecutionRepository()

    # Núcleo
    orchestrator = Orchestrator(repository)

    # Agentes
    task_agent = TaskAgent("Task_Agent")
    decision_agent = DecisionAgent("Decision_Agent")

    orchestrator.add_agent(task_agent)
    orchestrator.add_agent(decision_agent)

    # Reglas
    rule = Rule(
        condition=lambda state: state.get("objective") == Objective.PROCESS,
        action_agent_name="Decision_Agent"
    )

    orchestrator.add_rule(rule)

    return orchestrator