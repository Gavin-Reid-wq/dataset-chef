"""Tests for the tokenizer module."""

import pytest

from dataset_chef.tokenizer import count_tokens, count_tokens_in_row, get_tokenizer


def test_get_tokenizer() -> None:
    """Test tokenizer initialization."""
    tokenizer = get_tokenizer()
    assert tokenizer is not None

    # Test fallback
    tokenizer = get_tokenizer("invalid-model")
    assert tokenizer is not None


def test_count_tokens() -> None:
    """Test token counting."""
    text = "Hello, world!"
    tokens = count_tokens(text)
    assert tokens > 0

    # Test empty string
    assert count_tokens("") == 0

    # Test long text
    long_text = "Hello, world! " * 100
    tokens = count_tokens(long_text)
    assert tokens > 0


def test_count_tokens_in_row() -> None:
    """Test token counting in rows."""
    row = {
        "id": 1,
        "name": "test",
        "description": "This is a test description.",
    }
    tokens = count_tokens_in_row(row)
    assert tokens > 0

    # Test empty row
    assert count_tokens_in_row({}) == 0

    # Test row with non-string values
    row = {"id": 1, "name": "test", "value": 100}
    tokens = count_tokens_in_row(row)
    assert tokens > 0


def test_missing_tiktoken() -> None:
    """Test behavior when tiktoken is not installed."""
    import sys
    from unittest.mock import patch

    with patch.dict(sys.modules, {"tiktoken": None}):
        with pytest.raises(ImportError):
            count_tokens("test") 