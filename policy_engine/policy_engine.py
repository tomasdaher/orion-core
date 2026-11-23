from policy_engine.policy_registry import PolicyRegistry
from policy_engine.policy_evaluator import PolicyEvaluator


class PolicyEngine:

    def __init__(self):

        self.registry = PolicyRegistry()
        self.evaluator = PolicyEvaluator(self.registry)

    def register_policy(self, policy):

        self.registry.register(policy)

    def run(self, context):

        print("⚖️ Running policy evaluation")

        results = self.evaluator.evaluate(context)

        return results