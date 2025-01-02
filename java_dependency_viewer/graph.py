"""
Module for creating and managing dependency graphs of Java classes.

This module provides the Graph class which can build a visual representation
of class dependencies from Java bytecode files.
"""

import os
import json
import logging
import networkx as nx

from java_dependency_viewer.analyzer import Analyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Graph(nx.DiGraph):
    """
    A directed graph representing Java class dependencies.

    Extends networkx.DiGraph to store nodes (class names) and edges (dependencies between classes),
    and provides methods to build and export the graph structure.
    """

    def __init__(self):
        super().__init__()
        self.analyzer = Analyzer()

    def load_from_folder(self, class_dir_path: str):
        """
        Load class dependencies from a folder and build the graph.

        Args:
            class_dir_path: Path to directory containing Java class files
        """
        logging.info("Loading dependencies from %s", class_dir_path)
        nodes_set = set()
        class_dependencies = self.analyzer.analyze_from_class_dir(class_dir_path)
        for class_name, dependencies in class_dependencies.items():
            nodes_set.add(class_name)
            for dependency in dependencies:
                self.add_edge(class_name, dependency)
                logging.debug("Added edge: %s -> %s", class_name, dependency)

        edges_to_remove = [(u, v) for u, v in self.edges if v not in nodes_set]
        if edges_to_remove:
            logging.info(
                "Removing %d edges to external dependencies", len(edges_to_remove)
            )
        self.remove_edges_from(edges_to_remove)
        self.remove_nodes_from(self.nodes - nodes_set)
        logging.info(
            "Graph built with %d nodes and %d edges", len(self.nodes), len(self.edges)
        )

    def to_json(self) -> str:
        """
        Convert the Graph instance to JSON data format for vis.js.
        """
        logging.info("Converting graph to JSON format")
        nodes = [{"id": node, "label": node} for node in self.nodes]
        edges = [{"from": u, "to": v} for u, v in self.edges]
        return json.dumps({"nodes": nodes, "edges": edges})


if __name__ == "__main__":
    graph = Graph()
    graph.load_from_folder(
        os.path.join(os.path.dirname(__file__), os.pardir, "tests", "data", "classes")
    )

    logging.info("Nodes:")
    logging.info(list(graph.nodes))
    logging.info("Edges:")
    logging.info(list(graph.edges))
