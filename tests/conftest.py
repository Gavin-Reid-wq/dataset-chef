"""Pytest configuration and fixtures."""

import json
from pathlib import Path

import pytest


@pytest.fixture
def csv_file(tmp_path: Path) -> Path:
    """Create a temporary CSV file with test data."""
    file_path = tmp_path / "test.csv"
    with open(file_path, "w", newline="") as f:
        f.write("id,name,value\n")
        f.write("1,test1,100\n")
        f.write("2,test2,200\n")
        f.write("3,test1,300\n")
    return file_path


@pytest.fixture
def jsonl_file(tmp_path: Path) -> Path:
    """Create a temporary JSONL file with test data."""
    file_path = tmp_path / "test.jsonl"
    with open(file_path, "w") as f:
        for i in range(1, 4):
            f.write(json.dumps({"id": i, "name": f"test{i}", "value": i * 100}) + "\n")
    return file_path


@pytest.fixture
def large_file(tmp_path: Path) -> Path:
    """Create a temporary large file with test data."""
    file_path = tmp_path / "large.csv"
    with open(file_path, "w", newline="") as f:
        f.write("id,name,value\n")
        for i in range(1000):
            f.write(f"{i},test{i},{i * 100}\n")
    return file_path 