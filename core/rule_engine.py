class Rule:
    def __init__(self, condition, action_agent_name):
        self.condition = condition
        self.action_agent_name = action_agent_name

    def evaluate(self, state):
        return self.condition(state)