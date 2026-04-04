from collections import defaultdict
from capabilities.registry import CapabilityRegistry


class CapabilityGraph:

    def __init__(self):

        self.registry = CapabilityRegistry()

        # grafo de pasos
        self.graph = defaultdict(set)

        # mapa capability -> steps
        self.capability_map = {}

    def add_edge(self, node, next_step):

        self.graph[node].add(next_step)

    def build_graph(self):

        # limpiar grafo antes de reconstruir
        self.graph.clear()
        self.capability_map.clear()

        capabilities = self.registry.list_capabilities()

        for cap in capabilities:

            name = cap.get("name")
            steps = cap.get("steps", [])

            # guardar relación capability -> steps
            self.capability_map[name] = steps

            for i in range(len(steps) - 1):

                current_step = steps[i]
                next_step = steps[i + 1]

                self.graph[current_step].add(next_step)

        return self.graph

    def get_next_steps(self, step):

        if not self.capability_map:
            self.build_graph()

        return list(self.graph.get(step, []))

    def get_possible_paths(self, start_step, depth=3):

        if not self.capability_map:
            self.build_graph()

        paths = []

        def dfs(current_step, path, remaining_depth):

            if remaining_depth == 0:
                paths.append(path)
                return

            next_steps = self.graph.get(current_step, [])

            if not next_steps:
                paths.append(path)
                return

            for next_step in next_steps:

                dfs(
                    next_step,
                    path + [next_step],
                    remaining_depth - 1
                )

        dfs(start_step, [start_step], depth)

        return paths

    def get_capability_steps(self, capability_name):

        if not self.capability_map:
            self.build_graph()

        return self.capability_map.get(capability_name, [])

    def stats(self):

        if not self.capability_map:
            self.build_graph()

        return {
            "step_nodes": len(self.graph),
            "capabilities": len(self.capability_map)
        }

    def get_nodes(self):

        if not self.capability_map:
            self.build_graph()

        return list(self.graph.keys())

    def get_neighbors(self, node):

        if not self.capability_map:
            self.build_graph()

        return list(self.graph.get(node, []))