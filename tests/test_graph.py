import os
import unittest

from java_dependency_viewer.graph import Graph


class TestGraph(unittest.TestCase):
    def test_graph(self):
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
