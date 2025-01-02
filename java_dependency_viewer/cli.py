"""Command-line interface for Java Dependency Viewer."""

import argparse
import json
import logging
import os
import networkx as nx

from java_dependency_viewer.graph import Graph
from java_dependency_viewer.renderer import generate_html

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """Entry point for the jdv command."""
    parser = argparse.ArgumentParser(
        description="Analyze and visualize Java class dependencies"
    )
    parser.add_argument(
        "class_dir", help="Directory containing Java class files to analyze"
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="output",
        help="Directory to output the analysis results (default: output)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generate HTML visualization preview",
    )
    parser.add_argument(
        "--gexf",
        action="store_true",
        help="Export graph in GEXF format",
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Create and analyze graph
    logging.info("Analyzing Java classes in %s", args.class_dir)
    graph = Graph()
    graph.load_from_folder(args.class_dir)

    # Save graph data as JSON
    json_path = os.path.join(args.output_dir, "data.json")
    logging.info("Writing graph data to %s", json_path)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(nx.node_link_data(graph, edges="edges"), f)

    # Export GEXF if requested
    if args.gexf:
        gexf_path = os.path.join(args.output_dir, "data.gexf")
        logging.info("Writing GEXF file to %s", gexf_path)
        nx.write_gexf(graph, gexf_path)

    # Generate HTML preview if requested
    if args.preview:
        logging.info("Generating HTML preview")
        generate_html(args.class_dir, args.output_dir, json_exist=True)


if __name__ == "__main__":
    main()
