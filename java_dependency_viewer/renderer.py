"""
Module for rendering dependency graphs using different visualization libraries.

Provides functions to generate HTML visualizations using vis.js, sigma.js,
or cytoscape.js from the dependency graph data.
"""

import json
import os
import logging
from typing import Literal
import webbrowser

import networkx as nx

from java_dependency_viewer.graph import Graph

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_template(template_name: str) -> str:
    """
    Load the HTML template from a file.
    """
    template_path = os.path.join(os.path.dirname(__file__), template_name)
    logging.debug("Loading template from %s", template_path)
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()


def generate_html(
    folder_path: str,
    output_dir: str = ".",
    template_type: Literal["vis", "sigma", "cytoscape"] = "cytoscape",
    json_exist: bool = False,
):
    """
    Generate HTML visualization for Java class dependencies.

    Args:
        folder_path: Path to directory containing Java class files
        output_dir: Directory to output the generated files
        template_type: Type of visualization template to use
        json_exist: Whether to use existing data.json file
    """
    logging.info("Generating %s visualization for %s", template_type, folder_path)

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
        logging.info("Creating new graph from %s", folder_path)
        graph = Graph()
        graph.load_from_folder(folder_path)

        data_path = os.path.join(output_dir, "data.json")
        logging.info("Writing graph data to %s", data_path)
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(nx.node_link_data(graph, edges="edges"), f)

    html_path = os.path.join(output_dir, "graph.html")
    logging.info("Writing HTML to %s", html_path)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(template)

    logging.info("Opening visualization in browser")
    webbrowser.open(html_path)
