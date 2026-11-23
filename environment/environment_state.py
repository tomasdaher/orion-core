class EnvironmentState:

    def __init__(self):

        self.variables = {}
        self.entities = []
        self.timestamp = None

    def set_variable(self, key, value):

        self.variables[key] = value

    def get_variable(self, key, default=None):

        return self.variables.get(key, default)

    def add_entity(self, entity):

        self.entities.append(entity)

    def snapshot(self):

        return {
            "variables": self.variables,
            "entities": self.entities
        }