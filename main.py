from core.execution_request import Objective
from bootstrap import build_system
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():

    print("🚀 Iniciando Orion Core...")

    orchestrator = build_system()

    state = {
        "objective": Objective.PROCESS,
        "input": "example raw data"
    }

    orchestrator.handle_request(
        Objective.PROCESS,
        state
    )


if __name__ == "__main__":
    main()