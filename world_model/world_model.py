from world_model.entity_registry import EntityRegistry
from world_model.relation_graph import RelationGraph
from world_model.world_state import WorldState


class WorldModel:

    def __init__(self):

        self.registry = EntityRegistry()
        self.relations = RelationGraph()
        self.state = WorldState()

    def add_entity(self, entity):

        self.registry.register(entity)

    def relate(self, source, relation, target):

        self.relations.add_relation(
            source.id,
            relation,
            target.id
        )

    def snapshot(self):

        entities = self.registry.all()

        self.state.snapshot(entities)

        return self.state.get_state()