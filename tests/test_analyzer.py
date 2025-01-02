"""Tests for the Analyzer class."""

import logging
import os
import unittest

from java_dependency_viewer.analyzer import Analyzer

# Disable logging for tests
logging.disable(logging.CRITICAL)


class TestAnalyzer(unittest.TestCase):
    """Test cases for the Analyzer class."""

    log_path = os.path.join(os.path.dirname(__file__), "data", "App.log")
    class_path = os.path.join(
        os.path.dirname(__file__), "data", "classes", "com", "example", "App.class"
    )
    class_dir_path = os.path.join(os.path.dirname(__file__), "data", "classes")

    javap_output = ""

    @classmethod
    def setUpClass(cls):
        """Load test data before running tests."""
        with open(cls.log_path, "r", encoding="utf-8") as f:
            cls.javap_output = f.read()

    def test_analyze_from_str(self):
        """Test analyzing dependencies from javap output string."""
        analyzer = Analyzer()
        class_dependencies = analyzer.analyze_from_str(self.javap_output)
        self.assertDictEqual(
            class_dependencies,
            {
                "com.example.App": {
                    "com.example.Hoge",
                    "com.fuga.Fuga",
                    "java.lang.Object",
                }
            },
        )

    def test_analyze_from_class_dir(self):
        """Test analyzing dependencies from a directory of class files."""
        analyzer = Analyzer()
        class_dependencies = analyzer.analyze_from_class_dir(self.class_dir_path)
        self.assertDictEqual(
            class_dependencies,
            {
                "com.example.Hoge": {
                    "java.lang.Object",
                    "java.lang.System",
                    "java.io.PrintStream",
                },
                "com.example.App": {
                    "java.lang.Object",
                    "com.example.Hoge",
                    "com.fuga.Fuga",
                },
                "com.fuga.Fuga": {
                    "java.lang.System",
                    "java.lang.Object",
                    "java.io.PrintStream",
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
