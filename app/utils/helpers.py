"""
Helper Utilities
----------------
Reusable utility functions for:

- Formatting
- Safe conversions
- JSON responses
- Date utilities
"""

from datetime import datetime
from decimal import Decimal, InvalidOperation
from flask import jsonify


# ===============================
# SAFE FLOAT CONVERSION
# ===============================
def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


# ===============================
# SAFE DECIMAL CONVERSION
# ===============================
def safe_decimal(value, default=Decimal("0.00")):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return default


# ===============================
# FORMAT CURRENCY
# ===============================
def format_currency(amount, currency_symbol="$"):
    return f"{currency_symbol}{amount:,.2f}"


# ===============================
# FORMAT PERCENTAGE
# ===============================
def format_percentage(value):
    return f"{value:.2f}%"


# ===============================
# FORMAT DATE
# ===============================
def format_date(date_obj):
    if not isinstance(date_obj, datetime):
        return ""
    return date_obj.strftime("%d %b %Y")


# ===============================
# STANDARD JSON RESPONSE
# ===============================
def success_response(data, status=200):
    return jsonify({"status": "success", "data": data}), status


def error_response(message, status=400):
    return jsonify({"status": "error", "message": message}), status


# ===============================
# PERFORMANCE TIMER
# ===============================
def performance_timestamp():
    return datetime.utcnow().timestamp()