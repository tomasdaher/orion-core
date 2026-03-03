from core.orchestrator import Orchestrator
from core.rule_engine import Rule
from core.execution_request import ExecutionRequest, Objective
from agents.task_agent import TaskAgent
from agents.decision_agent import DecisionAgent
from infrastructure.repositories.json_execution_repository import JsonExecutionRepository


def main():
    print("🚀 Iniciando Orion Core...")

    repository = JsonExecutionRepository()
    orchestrator = Orchestrator(repository)

    # Registrar agentes
    task_agent = TaskAgent("Task_Agent")
    decision_agent = DecisionAgent("Decision_Agent")

    orchestrator.add_agent(task_agent)
    orchestrator.add_agent(decision_agent)

    # Crear regla basada en objetivo
    rule = Rule(
        condition=lambda state: state.get("objective") == Objective.PROCESS,
        action_agent_name="Decision_Agent"
    )

    orchestrator.add_rule(rule)

    # Crear request formal
    request = ExecutionRequest(
        objective=Objective.PROCESS,
        data={"input": "example raw data"}
    )

    # Ejecutar sistema
    orchestrator.execute(request)


if __name__ == "__main__":
    main()