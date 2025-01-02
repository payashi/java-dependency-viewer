"""
Module for creating and managing dependency graphs of Java classes.

This module provides the Graph class which can build a visual representation
of class dependencies from Java bytecode files.
"""

import os
import json

from java_dependency_viewer.analyzer import Analyzer


class Graph:
    """
    A class representing a dependency graph of Java classes.

    Stores nodes (class names) and edges (dependencies between classes),
    and provides methods to build and export the graph structure.
    """

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.analyzer = Analyzer()

    def add_node(self, node):
        """Add a node to the graph."""
        self.nodes.append(node)

    def add_edge(self, edge):
        """Add an edge to the graph."""
        self.edges.append(edge)

    def load_from_folder(self, class_dir_path: str):
        """
        Load class dependencies from a folder and build the graph.

        Args:
            class_dir_path: Path to directory containing Java class files
        """
        class_dependencies = self.analyzer.analyze_from_class_dir(class_dir_path)
        for class_name, dependencies in class_dependencies.items():
            self.add_node(class_name)
            for dependency in dependencies:
                self.add_edge((class_name, dependency))

        self._prune_edges()

    def _prune_edges(self):
        """Remove edges that point to non-existent nodes."""
        edges_to_remove = []
        for edge in self.edges:
            if edge[1] not in self.nodes:
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            self.edges.remove(edge)

    def to_json(self) -> str:
        """
        Convert the Graph instance to JSON data format for vis.js.
        """
        nodes = [{"id": node, "label": node} for node in self.nodes]
        edges = [{"from": edge[0], "to": edge[1]} for edge in self.edges]
        return json.dumps({"nodes": nodes, "edges": edges})


if __name__ == "__main__":
    graph = Graph()
    graph.load_from_folder(
        os.path.join(os.path.dirname(__file__), os.pardir, "tests", "data", "classes")
    )

    print(graph.nodes)
    print(graph.edges)
