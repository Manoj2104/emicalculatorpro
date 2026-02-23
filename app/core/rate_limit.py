"""
Advanced Rate Limiting
-----------------------
Provides dynamic rate limits based on:

- Authenticated user tier
- Guest IP address
- Configuration settings

Supports:
- Free tier limits
- Pro tier limits
- IP-based fallback
"""

from flask import request
from flask_login import current_user
from app.core.extensions import limiter


def user_rate_limit():
    """
    Dynamic rate limit logic.

    - Pro users: higher limit
    - Free users: medium limit
    - Guests: strict IP-based limit
    """

    if current_user.is_authenticated:
        if current_user.subscription_tier == "pro":
            return "200 per hour"
        else:
            return "50 per hour"

    # Guest fallback
    return "20 per hour"


def apply_dynamic_limit(route_function):
    """
    Apply dynamic rate limit decorator.
    Usage:

    @apply_dynamic_limit
    def api_route():
        ...
    """
    return limiter.limit(user_rate_limit)(route_function)