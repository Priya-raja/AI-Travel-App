import time
from typing import Any


_cache: dict[str, tuple[float, Any]] = {}


def get_cache(key: str) -> Any | None:
    """Return a cached value, or None when it is missing or expired."""
    entry = _cache.get(key)
    if entry is None:
        return None

    expires_at, value = entry
    if time.monotonic() >= expires_at:
        _cache.pop(key, None)
        return None

    return value


def set_cache(key: str, value: Any, ttl_seconds: float = 600) -> None:
    """Store a value in memory for the requested number of seconds."""
    if ttl_seconds <= 0:
        raise ValueError("ttl_seconds must be greater than zero")

    _cache[key] = (time.monotonic() + ttl_seconds, value)


def clear_cache() -> None:
    """Remove all cached values, primarily for tests and maintenance."""
    _cache.clear()
