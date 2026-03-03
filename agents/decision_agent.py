from core.execution_request import Objective


class DecisionAgent:
    def __init__(self, name):
        self.name = name

    def act(self, state):
        objective = state.get("objective")

        if objective == Objective.PROCESS:
            state.set("decision", "processing approved")
        elif objective == Objective.VALIDATE:
            state.set("decision", "validation approved")
        elif objective == Objective.EXECUTE:
            state.set("decision", "execution approved")
        else:
            state.set("decision", "no action")