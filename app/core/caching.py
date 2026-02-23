"""
Caching Configuration
----------------------
Handles application-level caching.

Supports:
- SimpleCache (Development)
- RedisCache (Production)
- Config-driven setup
- Utility decorator for manual caching
"""

from flask import current_app
from app.core.extensions import cache


def init_cache(app):
    """
    Initialize cache with app config.
    """

    cache.init_app(app)

    app.logger.info("Caching system initialized.")


def cache_key_builder(*args, **kwargs):
    """
    Custom cache key generator for complex queries.
    """

    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in kwargs.items()])

    return "emi_cache:" + "|".join(key_parts)


def clear_cache():
    """
    Clear all cache (admin usage).
    """
    cache.clear()


def get_cached_value(key):
    """
    Retrieve cached value safely.
    """
    return cache.get(key)


def set_cached_value(key, value, timeout=None):
    """
    Set cache value manually.
    """
    default_timeout = current_app.config.get("CACHE_DEFAULT_TIMEOUT", 300)
    cache.set(key, value, timeout or default_timeout)