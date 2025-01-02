import os
from typing import Literal
import webbrowser

from java_dependency_viewer.graph import Graph


def load_template(template_name: str) -> str:
    """
    Load the HTML template from a file.
    """
    template_path = os.path.join(os.path.dirname(__file__), template_name)
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()


def generate_html(
    folder_path: str,
    output_dir: str = ".",
    template_type: Literal["vis", "sigma", "cytoscape"] = "cytoscape",
    json_exist: bool = False,
):
    # Initialize template with default
    template = ""

    # Load the appropriate template based on the template_type
    if template_type == "vis":
        template = load_template("templates/vis_template.html")
    elif template_type == "sigma":
        template = load_template("templates/sigma_template.html")
    elif template_type == "cytoscape":
        template = load_template("templates/cytoscape_template.html")

    if not json_exist:
        graph = Graph()
        graph.load_from_folder(folder_path)

        vis_json_path = os.path.join(output_dir, "data.json")
        with open(vis_json_path, "w", encoding="utf-8") as f:
            f.write(graph.to_json())

    html_path = os.path.join(output_dir, "graph.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(template)

    webbrowser.open(html_path)
