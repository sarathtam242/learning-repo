def is_healthy(status_code: int) -> bool:
    """Return True when an HTTP status code indicates success."""
    return 200 <= status_code < 300