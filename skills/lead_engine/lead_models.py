import uuid
import time


class Lead:

    def __init__(self, name=None, email=None, company=None, source=None):

        self.id = str(uuid.uuid4())

        self.name = name
        self.email = email
        self.company = company
        self.source = source

        self.score = 0
        self.category = "unknown"

        self.created_at = time.time()

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "company": self.company,
            "source": self.source,
            "score": self.score,
            "category": self.category
        }