"""Utility functions for testing."""

# Builtins
from urllib.parse import urlparse


def is_valid_url(url):
    """Check if the url is valid."""
    result = urlparse(url)
    return all([result.scheme, result.netloc, result.path])
