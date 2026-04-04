from capabilities.capability_graph import CapabilityGraph


class CapabilityGraphPlanner:

    def __init__(self):

        self.graph = CapabilityGraph()

    def build_pipeline(self, start_step=None, max_depth=5):

        nodes = self.graph.get_nodes()

        if not nodes:
            return None

        pipeline = []

        visited = set()

        current = start_step if start_step else nodes[0]

        depth = 0

        while current and depth < max_depth:

            if current in visited:
                break

            pipeline.append(current)

            visited.add(current)

            neighbors = self.graph.get_neighbors(current)

            if not neighbors:
                break

            current = neighbors[0]

            depth += 1

        if len(pipeline) <= 1:
            return None

        return pipeline