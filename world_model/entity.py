import uuid
import time


class Entity:

    def __init__(self, entity_type, attributes=None):

        self.id = str(uuid.uuid4())
        self.type = entity_type
        self.attributes = attributes or {}

        self.created_at = time.time()
        self.updated_at = time.time()

    def update(self, key, value):

        self.attributes[key] = value
        self.updated_at = time.time()

    def get(self, key, default=None):

        return self.attributes.get(key, default)

    def to_dict(self):

        return {
            "id": self.id,
            "type": self.type,
            "attributes": self.attributes
        }