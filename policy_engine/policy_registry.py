class PolicyRegistry:

    def __init__(self):

        self.policies = []

    def register(self, policy):

        print(f"📜 Policy registered: {policy.name}")

        self.policies.append(policy)

    def all(self):

        return self.policies