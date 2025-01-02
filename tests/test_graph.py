"""Tests for the Graph class."""

import logging
import os
import unittest

from java_dependency_viewer.graph import Graph

# Disable logging for tests
logging.disable(logging.CRITICAL)


class TestGraph(unittest.TestCase):
    """Test cases for the Graph class."""

    def test_graph(self):
        """Test graph construction and dependency relationships."""
        graph = Graph()
        graph.load_from_folder(
            os.path.join(os.path.dirname(__file__), "data", "classes")
        )
        self.assertSetEqual(
            set(graph.nodes), {"com.example.App", "com.example.Hoge", "com.fuga.Fuga"}
        )
        self.assertSetEqual(
            set(graph.edges),
            {
                ("com.example.App", "com.example.Hoge"),
                ("com.example.App", "com.fuga.Fuga"),
            },
        )


if __name__ == "__main__":
    unittest.main()
