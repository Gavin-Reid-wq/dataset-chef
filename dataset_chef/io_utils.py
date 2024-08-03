"""I/O utilities for handling CSV and JSONL files."""

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Union

import click
from rich.console import Console

console = Console()


def detect_format(file_path: Union[str, Path]) -> str:
    """Detect file format based on extension."""
    ext = Path(file_path).suffix.lower()
    if ext == ".csv":
        return "csv"
    elif ext == ".jsonl":
        return "jsonl"
    raise ValueError(f"Unsupported file format: {ext}")


def stream_rows(
    file_path: Union[str, Path], format: Optional[str] = None
) -> Iterator[Dict[str, Any]]:
    """Stream rows from a CSV or JSONL file."""
    file_path = Path(file_path)
    format = format or detect_format(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        if format == "csv":
            reader = csv.DictReader(f)
            yield from reader
        elif format == "jsonl":
            for line in f:
                if line.strip():
                    yield json.loads(line)
        else:
            raise ValueError(f"Unsupported format: {format}")


def write_rows(
    file_path: Union[str, Path],
    rows: Iterator[Dict[str, Any]],
    format: Optional[str] = None,
) -> None:
    """Write rows to a CSV or JSONL file."""
    file_path = Path(file_path)
    format = format or detect_format(file_path)

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        if format == "csv":
            if not rows:
                return
            first_row = next(rows)
            writer = csv.DictWriter(f, fieldnames=first_row.keys())
            writer.writeheader()
            writer.writerow(first_row)
            writer.writerows(rows)
        elif format == "jsonl":
            for row in rows:
                f.write(json.dumps(row) + "\n")
        else:
            raise ValueError(f"Unsupported format: {format}")


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print_json(json.dumps(data))


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """Print data as a formatted table."""
    from rich.table import Table

    table = Table(*headers)
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    console.print(table) 