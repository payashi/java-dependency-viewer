import json

from java_dependency_viewer.analyzer import Analyzer


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.analyzer = Analyzer()

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def load_from_folder(self, class_dir_path: str):
        class_dependencies = self.analyzer.analyze_from_class_dir(class_dir_path)
        for class_name, dependencies in class_dependencies.items():
            self.add_node(class_name)
            for dependency in dependencies:
                self.add_edge((class_name, dependency))

        self._prune_edges()

    def _prune_edges(self):
        edges_to_remove = []
        for edge in self.edges:
            if edge[1] not in self.nodes:
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            self.edges.remove(edge)

    def to_json(self) -> str:
        """
        Graphインスタンスをvis.js用のJSONデータ形式に変換します。
        """
        nodes = [{"id": node, "label": node} for node in self.nodes]
        edges = [{"from": edge[0], "to": edge[1]} for edge in self.edges]
        return json.dumps({"nodes": nodes, "edges": edges})


if __name__ == "__main__":
    graph = Graph()
    graph.load_from_folder(
        "/Users/payashi/Documents/java-playground/guava/guava/target/classes/com/google/common/escape"
    )

    print(graph.nodes)
    print(graph.edges)
