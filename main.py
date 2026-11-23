from core.execution_request import Objective
from bootstrap import build_system
from core.cognition.cognitive_loop import CognitiveLoop
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

    loop = CognitiveLoop(orchestrator)

    loop.run(state)


if __name__ == "__main__":
    main()