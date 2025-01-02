"""
This module provides the Analyzer class for extracting class dependencies
from Java class files using the `javap` tool.

The Analyzer class can process individual Java class files or entire directories
containing class files to extract the target class and its dependent classes.
"""

from concurrent.futures import ThreadPoolExecutor
import os
import re
import logging
import subprocess
from typing import Dict, Iterable, List, Set, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Analyzer:
    """
    Analyzer class to extract class dependencies from Java class files.

    This class provides methods to analyze Java class files and extract
    the target class and its dependent classes using the output from the
    `javap` tool. It can process individual class files or entire directories
    containing class files.
    """

    def __init__(self):
        # Precompile regular expressions
        self.this_class_pattern = re.compile(r"this_class:\s+#\d+\s+//\s+([\w/.$]+)")
        self.constant_pool_pattern = re.compile(
            r"#\d+\s+=\s+Class\s+#\d+\s+//\s+([\w/.$]+)"
        )

    def analyze_from_str(self, javap_output: str) -> Dict[str, Set[str]]:
        """
        Extract target class and dependent classes from javap output.
        """
        logging.info("Analyzing class files...")
        # Split the log by sections
        sections = javap_output.split("Constant pool:")
        if len(sections) < 2:
            logging.error(
                "Invalid javap output format. 'Constant pool' section not found."
            )
            return {}

        # Get class name
        this_class_match = self.this_class_pattern.search(sections[0])
        if not this_class_match:
            logging.error("Invalid javap output format. 'this_class' not found.")
            return {}
        current_class = this_class_match.group(1).replace("/", ".")

        # Parse the Constant pool to get dependent classes
        dependencies = set()
        constant_pool_section = sections[1]
        constant_pool_matches = self.constant_pool_pattern.findall(
            constant_pool_section
        )
        for match in constant_pool_matches:
            dependencies.add(match.replace("/", "."))
        dependencies.discard(current_class)

        return {current_class: dependencies}

    def analyze_from_class_dir(self, class_dir_path: str) -> Dict[str, Set[str]]:
        """
        Analyze all Java class files in a directory and extract their dependencies.

        Args:
            class_dir_path: Path to directory containing Java class files

        Returns:
            Dictionary mapping class names to their dependencies
        """
        logging.info("Analyzing class files in %s", class_dir_path)
        class_paths = []
        for root, _, files in os.walk(class_dir_path):
            for file in files:
                if file.endswith(".class"):
                    class_paths.append(os.path.join(root, file))
        source_file_all = self.run(class_paths)

        sections = self._split_sections(source_file_all)

        with ThreadPoolExecutor() as executor:
            results: List[Dict[str, Set[str]]] = list(
                executor.map(self.analyze_from_str, sections)
            )

        results = {key: value for result in results for key, value in result.items()}
        return results

    def _split_sections(self, source: str) -> Iterable[str]:
        """Split javap output into sections by class file."""
        classfile_pattern = re.compile(r"\nClassfile.*\n")
        sections = re.split(classfile_pattern, source)
        return sections

    def run(self, class_paths: Union[str, Iterable[str]]) -> str:
        """
        Run javap command on given class files and return output.

        Args:
            class_paths: Path(s) to Java class file(s)

        Returns:
            Output from javap command as string
        """
        logging.info("Running javap on %s", class_paths)
        if isinstance(class_paths, str):
            class_paths = [class_paths]
        try:
            # Use subprocess.run to execute javap
            result = subprocess.run(
                ["javap", "-verbose", *class_paths],  # javap command and arguments
                capture_output=True,  # Capture standard output and error output
                text=True,  # Get output as a string
                check=True,  # Raise an exception on error
            )
            return result.stdout  # Return standard output
        except subprocess.CalledProcessError as e:
            logging.error("Error running javap: %s", e.stderr)
            raise


# Example usage
if __name__ == "__main__":
    test_class_dir = os.path.join(
        os.path.dirname(__file__), os.pardir, "tests", "data", "classes", "com"
    )
    try:
        analyzer = Analyzer()
        class_dependencies = analyzer.analyze_from_class_dir(test_class_dir)
        logging.info("Class dependencies: %s", class_dependencies)
    except (subprocess.CalledProcessError, ValueError) as e:
        logging.error("Failed to analyze class file: %s", e)
