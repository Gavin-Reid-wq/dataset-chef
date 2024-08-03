"""Tests for the CLI module."""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from dataset_chef.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner."""
    return CliRunner()


def test_slice_command(runner: CliRunner, csv_file: Path, tmp_path: Path) -> None:
    """Test the slice command."""
    output = tmp_path / "output.csv"
    result = runner.invoke(main, ["slice", "-i", str(csv_file), "-o", str(output), "-n", "2"])
    assert result.exit_code == 0
    assert "Total Rows" in result.output
    assert "Sliced Rows" in result.output

    # Test JSON output
    result = runner.invoke(
        main, ["slice", "-i", str(csv_file), "-o", str(output), "-n", "2", "--json"]
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "total_rows" in data
    assert "sliced_rows" in data


def test_dedup_command(runner: CliRunner, csv_file: Path, tmp_path: Path) -> None:
    """Test the dedup command."""
    output = tmp_path / "output.csv"
    result = runner.invoke(main, ["dedup", "-i", str(csv_file), "-o", str(output)])
    assert result.exit_code == 0
    assert "Total Rows" in result.output
    assert "Unique Rows" in result.output
    assert "Duplicates" in result.output

    # Test with key
    result = runner.invoke(
        main, ["dedup", "-i", str(csv_file), "-o", str(output), "-k", "name"]
    )
    assert result.exit_code == 0

    # Test JSON output
    result = runner.invoke(
        main, ["dedup", "-i", str(csv_file), "-o", str(output), "--json"]
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "total_rows" in data
    assert "unique_rows" in data


def test_token_count_command(runner: CliRunner, csv_file: Path) -> None:
    """Test the token-count command."""
    result = runner.invoke(main, ["token-count", "-i", str(csv_file)])
    assert result.exit_code == 0
    assert "Total Tokens" in result.output
    assert "Total Rows" in result.output

    # Test JSON output
    result = runner.invoke(main, ["token-count", "-i", str(csv_file), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "total_tokens" in data
    assert "total_rows" in data


def test_stats_command(runner: CliRunner, csv_file: Path) -> None:
    """Test the stats command."""
    result = runner.invoke(main, ["stats", "-i", str(csv_file)])
    assert result.exit_code == 0
    assert "Total Rows" in result.output

    # Test with column
    result = runner.invoke(main, ["stats", "-i", str(csv_file), "-c", "name"])
    assert result.exit_code == 0

    # Test JSON output
    result = runner.invoke(main, ["stats", "-i", str(csv_file), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "total_rows" in data
    assert "columns" in data 