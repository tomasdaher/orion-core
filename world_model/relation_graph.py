class RelationGraph:

    def __init__(self):

        self.relations = []

    def add_relation(self, source_id, relation_type, target_id):

        relation = {
            "source": source_id,
            "type": relation_type,
            "target": target_id
        }

        self.relations.append(relation)

    def get_relations(self, entity_id):

        return [
            r for r in self.relations
            if r["source"] == entity_id
        ]