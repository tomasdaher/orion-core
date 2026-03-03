from core.execution_request import ExecutionRequest, Objective
from bootstrap import build_system


def main():
    print("🚀 Iniciando Orion Core...")

    orchestrator = build_system()

    request = ExecutionRequest(
        objective=Objective.PROCESS,
        data={"input": "example raw data"}
    )

    orchestrator.execute(request)


if __name__ == "__main__":
    main()