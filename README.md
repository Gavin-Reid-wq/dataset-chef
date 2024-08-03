# Dataset Chef 🧑‍🍳

<!--
<svg width="100" height="100" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="45" fill="#FFD700"/>
  <text x="50" y="65" text-anchor="middle" font-size="60">👨‍🍳</text>
</svg>
-->

[![PyPI version](https://badge.fury.io/py/dataset-chef.svg)](https://badge.fury.io/py/dataset-chef)
[![Python Versions](https://img.shields.io/pypi/pyversions/dataset-chef.svg)](https://pypi.org/project/dataset-chef/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/yourusername/dataset-chef/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/dataset-chef/actions/workflows/ci.yml)
[![Code Coverage](https://codecov.io/gh/yourusername/dataset-chef/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/dataset-chef)

A command-line tool for dataset processing and analysis. Stream your data, never load it all in memory!

## Features

- 🚀 Stream large datasets efficiently
- 📊 Support for CSV and JSONL formats
- 🔍 Fast hash-based deduplication
- 📝 Token counting with tiktoken
- 📈 Basic dataset statistics
- 🎨 Beautiful console output

## Installation

```bash
pip install dataset-chef
```

## Quick Start

```bash
# Slice a dataset to first 1000 rows
dataset-chef slice -i input.csv -o output.csv -n 1000

# Remove duplicates based on a column
dataset-chef dedup -i input.jsonl -o output.jsonl -k name

# Count tokens in a dataset
dataset-chef token-count -i input.csv

# Get dataset statistics
dataset-chef stats -i input.jsonl
```

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Input     │     │  Process    │     │   Output    │
│  (CSV/JSONL)│────▶│  (Stream)   │────▶│  (CSV/JSONL)│
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                    ┌─────┴─────┐
                    │  Stats    │
                    │  Tokens   │
                    └───────────┘
```

## Development

1. Clone the repository
2. Install dependencies: `poetry install`
3. Run tests: `poetry run pytest`
4. Run linting: `poetry run pre-commit run --all-files`

## License

MIT License - see [LICENSE](LICENSE) for details. 