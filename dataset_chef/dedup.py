"""Deduplication utilities for datasets."""

import hashlib
from typing import Any, Dict, Iterator, Optional, Set

from .io_utils import stream_rows, write_rows


def hash_row(row: Dict[str, Any], key: Optional[str] = None) -> str:
    """Hash a row using its values or a specific key."""
    if key:
        value = str(row.get(key, ""))
    else:
        value = "|".join(str(v) for v in row.values())
    return hashlib.sha256(value.encode()).hexdigest()


def deduplicate(
    input_path: str,
    output_path: str,
    key: Optional[str] = None,
    seen: Optional[Set[str]] = None,
) -> tuple[int, int]:
    """Deduplicate rows from input file and write to output file."""
    seen = seen or set()
    total = 0
    unique = 0

    def dedup_generator() -> Iterator[Dict[str, Any]]:
        nonlocal total, unique
        for row in stream_rows(input_path):
            total += 1
            row_hash = hash_row(row, key)
            if row_hash not in seen:
                seen.add(row_hash)
                unique += 1
                yield row

    write_rows(output_path, dedup_generator())
    return total, unique 