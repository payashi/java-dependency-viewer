"""Example script demonstrating the usage of java-dependency-viewer."""

import os

from java_dependency_viewer.renderer import generate_html

OUTPUT_DIR = "dist"
os.makedirs(OUTPUT_DIR, exist_ok=True)

test_class_dir = os.path.join(
    os.path.dirname(__file__), os.pardir, "tests", "data", "classes"
)

generate_html(
    test_class_dir,
    OUTPUT_DIR,
    json_exist=False,
)
