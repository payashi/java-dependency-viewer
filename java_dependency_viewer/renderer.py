import os
from typing import Literal
import webbrowser

from java_dependency_viewer.graph import Graph

CYTOSCAPE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cytoscape.js Network</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js"></script>
    <script src="https://unpkg.com/layout-base/layout-base.js"></script>
    <script src="https://unpkg.com/cose-base/cose-base.js"></script>
    <script src="https://unpkg.com/cytoscape-fcose/cytoscape-fcose.js"></script>
    <style>
        #cy {
            width: 100%;
            height: 800px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div id="cy"></div>

    <script>
        // Fetch JSON data and render the network
        fetch('data.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const elements = {
                    nodes: data.nodes.map(node => ({
                        data: { id: node.id, label: node.label }
                    })),
                    edges: data.edges.map(edge => ({
                        data: { source: edge.from, target: edge.to }
                    }))
                };

                // Initialize Cytoscape
                const cy = cytoscape({
                    container: document.getElementById('cy'),
                    elements: elements,
                    layout: {
                        name: 'fcose',
                        animate: true,
                    },
                    style: [
                        {
                            selector: 'node',
                            style: {
                                'background-color': '#0074D9',
                                // 'label': 'data(label)',
                                'text-valign': 'center',
                                'color': '#000000'
                            }
                        },
                        {
                            selector: 'edge',
                            style: {
                                'line-color': '#AAAAAA',
                                'target-arrow-color': '#AAAAAA',
                                'target-arrow-shape': 'triangle',
                                'curve-style': 'bezier',
                            }
                        }
                    ]
                });
            })
            .catch(error => {
                console.error('Error fetching or rendering the network:', error);
            });
    </script>
</body>
</html>
"""

VIS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Graph Visualization</title>
    <script
    type="text/javascript"
    src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"
    ></script>
</head>
<body>
    <div id="network" style="width: 100%; height: 800px; border: 1px solid lightgray;"></div>
    <script>
        fetch('data.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const container = document.getElementById('network');
                const options = {
                    edges: {
                        arrows: {
                            to: { enabled: true, scaleFactor: 1.2 }
                        },
                        smooth: true
                    },
                    nodes: {
                        shape: 'dot',
                        size: 10
                    },
                    physics: {
                        enabled: true
                    }
                };
                const network = new vis.Network(container, data, options);
            })
            .catch(error => {
                console.error('Error fetching or rendering the network:', error);
            });
    </script>
</body>
</html>
"""

SIGMA_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sigma.js Network</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/2.4.0/sigma.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/graphology/0.25.4/graphology.umd.min.js"></script>
    <style>
        #container {
            width: 100%;
            height: 800px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div id="container" ></div>
    <script>
    // Fetch JSON data and render the graph
    fetch('data.json')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Create a graphology graph
        const graph = new graphology.Graph();

        // Add nodes
        data.nodes.forEach(node => {
          graph.addNode(node.id, {
            label: node.label,
            x: Math.random(), // ランダムな座標
            y: Math.random(),
            size: 10,
            color: "blue"
          });
        });

        // Add edges
        data.edges.forEach(edge => {
          graph.addEdge(edge.from, edge.to, {
            color: "purple",
            size: 2
          });
        });

        // Instantiate sigma.js and render the graph
        const sigmaInstance = new Sigma(graph, document.getElementById("container"));
      })
      .catch(error => {
        console.error('Error fetching or rendering the graph:', error);
      });
    </script>
</body>
</html>
"""


def generate_html(
    folder_path: str,
    output_dir: str = ".",
    template_type: Literal["vis", "sigma", "cytoscape"] = "vis",
    json_exist: bool = False,
):

    if template_type == "vis":
        template = VIS_TEMPLATE
    elif template_type == "sigma":
        template = SIGMA_TEMPLATE
    elif template_type == "cytoscape":
        template = CYTOSCAPE_TEMPLATE

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
