"""Tokenizer utilities using tiktoken."""

from typing import Dict, Optional

try:
    import tiktoken
except ImportError:
    tiktoken = None


def get_tokenizer(model: str = "gpt-3.5-turbo") -> Optional[tiktoken.Encoding]:
    """Get a tiktoken tokenizer for the specified model."""
    if tiktoken is None:
        return None
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count tokens in text using tiktoken."""
    tokenizer = get_tokenizer(model)
    if tokenizer is None:
        raise ImportError(
            "tiktoken is not installed. Install it with: pip install tiktoken"
        )
    return len(tokenizer.encode(text))


def count_tokens_in_row(row: Dict[str, str], model: str = "gpt-3.5-turbo") -> int:
    """Count tokens in all string values of a row."""
    return sum(count_tokens(str(v), model) for v in row.values() if isinstance(v, str)) 