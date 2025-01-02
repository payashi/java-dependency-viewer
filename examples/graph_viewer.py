import os

from java_dependency_viewer.renderer import generate_html

output_dir = "dist"
os.makedirs(output_dir, exist_ok=True)

generate_html(
    "/Users/payashi/Documents/java-playground/guava/guava/target/classes/com/google/common/escape",
    output_dir,
    template_type="cytoscape",
    json_exist=False,
)
