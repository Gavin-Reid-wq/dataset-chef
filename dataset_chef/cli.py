"""Command-line interface for dataset-chef."""

import itertools
from typing import Any, Dict, Optional

import click
from rich.console import Console

from . import __version__
from .dedup import deduplicate
from .io_utils import print_json, print_table, stream_rows
from .stats import get_column_stats, get_token_stats

console = Console()


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Dataset Chef - A command-line tool for dataset processing and analysis."""
    pass


@main.command()
@click.option("--input", "-i", required=True, help="Input file path")
@click.option("--output", "-o", required=True, help="Output file path")
@click.option("--max-lines", "-n", type=int, help="Maximum number of lines to process")
@click.option("--json", is_flag=True, help="Output in JSON format")
def slice(input: str, output: str, max_lines: Optional[int], json: bool) -> None:
    """Slice a dataset to a maximum number of lines."""
    rows = itertools.islice(stream_rows(input), max_lines)
    total = sum(1 for _ in stream_rows(input))
    sliced = sum(1 for _ in stream_rows(output))

    if json:
        print_json({"total_rows": total, "sliced_rows": sliced})
    else:
        print_table(
            ["Metric", "Value"],
            [
                ["Total Rows", total],
                ["Sliced Rows", sliced],
            ],
        )


@main.command()
@click.option("--input", "-i", required=True, help="Input file path")
@click.option("--output", "-o", required=True, help="Output file path")
@click.option("--key", "-k", help="Column to use for deduplication")
@click.option("--json", is_flag=True, help="Output in JSON format")
def dedup(input: str, output: str, key: Optional[str], json: bool) -> None:
    """Remove duplicate rows from a dataset."""
    total, unique = deduplicate(input, output, key)

    if json:
        print_json({"total_rows": total, "unique_rows": unique})
    else:
        print_table(
            ["Metric", "Value"],
            [
                ["Total Rows", total],
                ["Unique Rows", unique],
                ["Duplicates", total - unique],
            ],
        )


@main.command()
@click.option("--input", "-i", required=True, help="Input file path")
@click.option("--model", "-m", default="gpt-3.5-turbo", help="Model to use for tokenization")
@click.option("--json", is_flag=True, help="Output in JSON format")
def token_count(input: str, model: str, json: bool) -> None:
    """Count tokens in a dataset."""
    stats = get_token_stats(input, model)

    if json:
        print_json(stats)
    else:
        print_table(
            ["Metric", "Value"],
            [
                ["Total Tokens", stats["total_tokens"]],
                ["Total Rows", stats["total_rows"]],
                ["Avg Tokens/Row", f"{stats['avg_tokens_per_row']:.1f}"],
                ["Min Tokens", stats["min_tokens"]],
                ["Max Tokens", stats["max_tokens"]],
            ],
        )


@main.command()
@click.option("--input", "-i", required=True, help="Input file path")
@click.option("--column", "-c", help="Column to analyze")
@click.option("--json", is_flag=True, help="Output in JSON format")
def stats(input: str, column: Optional[str], json: bool) -> None:
    """Get statistics about a dataset."""
    stats = get_column_stats(input, column)

    if json:
        print_json(stats)
    else:
        rows = [["Total Rows", stats["total_rows"]]]
        for col, values in stats["columns"].items():
            if isinstance(values, dict):
                rows.append([f"Unique {col}", len(values)])
                rows.append([f"Most common {col}", max(values.items(), key=lambda x: x[1])[0]])
        print_table(["Metric", "Value"], rows)


if __name__ == "__main__":
    main() 