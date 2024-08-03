"""Tests for the deduplication module."""

from pathlib import Path

import pytest

from dataset_chef.dedup import deduplicate, hash_row


def test_hash_row() -> None:
    """Test row hashing."""
    row = {"id": 1, "name": "test", "value": 100}
    hash1 = hash_row(row)
    hash2 = hash_row(row)
    assert hash1 == hash2

    # Test with key
    hash3 = hash_row(row, "name")
    assert hash3 != hash1


def test_deduplicate(csv_file: Path, tmp_path: Path) -> None:
    """Test deduplication."""
    output = tmp_path / "output.csv"
    total, unique = deduplicate(str(csv_file), str(output))
    assert total == 3
    assert unique == 3

    # Test with duplicates
    with open(csv_file, "a") as f:
        f.write("4,test1,400\n")  # Duplicate name
    total, unique = deduplicate(str(csv_file), str(output), key="name")
    assert total == 4
    assert unique == 2  # Only 2 unique names


def test_deduplicate_large_file(large_file: Path, tmp_path: Path) -> None:
    """Test deduplication with a large file."""
    output = tmp_path / "output.csv"
    total, unique = deduplicate(str(large_file), str(output))
    assert total == 1000
    assert unique == 1000

    # Add some duplicates
    with open(large_file, "a") as f:
        for i in range(100):
            f.write(f"{i},test{i},{i * 100}\n")
    total, unique = deduplicate(str(large_file), str(output))
    assert total == 1100
    assert unique == 1000 