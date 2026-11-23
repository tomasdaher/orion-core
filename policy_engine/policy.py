class Policy:

    def __init__(self, name, condition, action):

        self.name = name
        self.condition = condition
        self.action = action

    def evaluate(self, context):

        try:

            if self.condition(context):

                return self.action(context)

        except Exception as e:

            print(f"❌ Policy error: {self.name} | {e}")

        return None