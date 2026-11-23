class PolicyEvaluator:

    def __init__(self, registry):

        self.registry = registry

    def evaluate(self, context):

        results = []

        for policy in self.registry.all():

            result = policy.evaluate(context)

            if result:

                results.append(result)

        return results