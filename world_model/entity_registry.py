class EntityRegistry:

    def __init__(self):

        self.entities = {}

    def register(self, entity):

        self.entities[entity.id] = entity

    def get(self, entity_id):

        return self.entities.get(entity_id)

    def all(self):

        return list(self.entities.values())

    def by_type(self, entity_type):

        return [
            e for e in self.entities.values()
            if e.type == entity_type
        ]