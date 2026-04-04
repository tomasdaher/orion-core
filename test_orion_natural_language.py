import logging

from core.orchestrator import Orchestrator
from core.capability_registry import CapabilityRegistry


# ------------------------------------------------
# Dummy repository
# ------------------------------------------------
class DummyRepository:

    def save_execution(self, state):

        print("\n💾 Execution saved")


# ------------------------------------------------
# Logging setup
# ------------------------------------------------
def setup_logging():

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s"
    )


# ------------------------------------------------
# MAIN TEST
# ------------------------------------------------
def main():

    print("\n🚀 Orion Natural Language Test\n")

    setup_logging()

    # ------------------------------------------------
    # Repository
    # ------------------------------------------------
    repository = DummyRepository()

    # ------------------------------------------------
    # Registry
    # ------------------------------------------------
    registry = CapabilityRegistry()

    # ------------------------------------------------
    # Orchestrator
    # ------------------------------------------------
    orchestrator = Orchestrator(
        repository=repository,
        capability_registry=registry
    )

    # ------------------------------------------------
    # NATURAL LANGUAGE INSTRUCTION
    # ------------------------------------------------
    instruction = """
    capture leads from instagram
    clean them
    classify them
    store them
    and notify hot leads
    """

    print("🧠 Instruction:")
    print(instruction)

    # ------------------------------------------------
    # EXECUTE
    # ------------------------------------------------
    result = orchestrator.run_text(instruction)

    print("\n✅ Execution finished\n")

    print("📊 Final state:\n")

    print(result)


if __name__ == "__main__":
    main()