"""Dataset statistics utilities."""

from collections import Counter
from typing import Any, Dict, List, Optional

from .io_utils import stream_rows
from .tokenizer import count_tokens_in_row


def get_column_stats(
    input_path: str, column: Optional[str] = None
) -> Dict[str, Any]:
    """Get statistics for a specific column or all columns."""
    stats: Dict[str, Any] = {
        "total_rows": 0,
        "columns": {},
    }

    for row in stream_rows(input_path):
        stats["total_rows"] += 1

        if column:
            value = row.get(column)
            if value not in stats["columns"]:
                stats["columns"][value] = 0
            stats["columns"][value] += 1
        else:
            for col, value in row.items():
                if col not in stats["columns"]:
                    stats["columns"][col] = Counter()
                stats["columns"][col][value] += 1

    # Convert Counter objects to dicts for JSON serialization
    if not column:
        for col in stats["columns"]:
            stats["columns"][col] = dict(stats["columns"][col])

    return stats


def get_token_stats(input_path: str, model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
    """Get token statistics for the dataset."""
    total_tokens = 0
    total_rows = 0
    token_counts: List[int] = []

    for row in stream_rows(input_path):
        total_rows += 1
        row_tokens = count_tokens_in_row(row, model)
        total_tokens += row_tokens
        token_counts.append(row_tokens)

    if not token_counts:
        return {
            "total_tokens": 0,
            "total_rows": 0,
            "avg_tokens_per_row": 0,
            "min_tokens": 0,
            "max_tokens": 0,
        }

    return {
        "total_tokens": total_tokens,
        "total_rows": total_rows,
        "avg_tokens_per_row": total_tokens / total_rows,
        "min_tokens": min(token_counts),
        "max_tokens": max(token_counts),
    } 