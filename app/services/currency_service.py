"""
Currency Conversion Service
-----------------------------
Handles multi-currency conversion with:

- Cached exchange rates
- Fallback offline rates
- API-ready structure
- Performance optimized
- Scalable to Redis caching

Note:
In production, integrate real Forex API like:
- exchangerate-api
- fixer.io
- openexchangerates
"""

import requests
from decimal import Decimal, ROUND_HALF_UP
from flask import current_app
from app.core.extensions import cache


class CurrencyService:

    # Fallback static rates (base: USD)
    FALLBACK_RATES = {
        "USD": 1.0,
        "INR": 83.0,
        "EUR": 0.92,
        "GBP": 0.78,
        "AUD": 1.50,
        "CAD": 1.35
    }

    @staticmethod
    def _round(value):
        precision = current_app.config.get("DECIMAL_PRECISION", 2)
        return float(
            Decimal(value).quantize(
                Decimal("1." + "0" * precision),
                rounding=ROUND_HALF_UP
            )
        )

    @staticmethod
    @cache.cached(timeout=3600, key_prefix="forex_rates")
    def get_live_rates():
        """
        Fetch live exchange rates.
        Cached for 1 hour.
        """

        try:
            # Example public API (replace with production API)
            response = requests.get(
                "https://open.er-api.com/v6/latest/USD",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("rates", CurrencyService.FALLBACK_RATES)

        except Exception:
            pass

        return CurrencyService.FALLBACK_RATES

    @staticmethod
    def convert(amount, from_currency="USD", to_currency="USD"):
        """
        Convert amount between currencies.
        """

        rates = CurrencyService.get_live_rates()

        if from_currency not in rates or to_currency not in rates:
            raise ValueError("Unsupported currency")

        # Convert to USD first (base)
        amount_in_usd = amount / rates[from_currency]

        # Convert to target currency
        converted = amount_in_usd * rates[to_currency]

        return {
            "original_amount": CurrencyService._round(amount),
            "from": from_currency,
            "to": to_currency,
            "converted_amount": CurrencyService._round(converted),
            "rate_used": CurrencyService._round(rates[to_currency])
        }

    @staticmethod
    def supported_currencies():
        """
        Return supported currency list.
        """

        rates = CurrencyService.get_live_rates()
        return sorted(list(rates.keys()))