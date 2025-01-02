# Java Dependency Viewer

A command-line tool for analyzing and visualizing Java class dependencies using javap.

## Installation

```bash
pip install java-dependency-viewer
```

## Usage

Basic command format:
```bash
jdv [class_dir] [output_dir] [options]
```

Arguments:
- `class_dir`: Directory containing Java class files to analyze (required)
- `output_dir`: Directory to output the analysis results (optional, default: output)

Options:
- `--preview`: Generate HTML visualization preview
- `--gexf`: Export graph in GEXF format

Examples:
```bash
# Basic usage (creates data.json in output/)
jdv path/to/classes

# Specify output directory
jdv path/to/classes output/

# Generate GEXF file
jdv path/to/classes --gexf

# Generate HTML preview
jdv path/to/classes --preview

# All options
jdv path/to/classes output/ --preview --gexf
```

## Output Files

- `data.json`: Graph data in JSON format (always created)
- `data.gexf`: Graph data in GEXF format (created with --gexf)
- `graph.html`: Interactive visualization (created with --preview)

## Requirements

- Python 3.6+
- Java Development Kit (JDK) with `javap` command available
- NetworkX 2.5+

## License

MIT License
