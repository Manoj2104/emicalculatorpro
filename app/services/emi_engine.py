"""
EMI Calculation Engine
-----------------------
Centralized financial computation engine.

Designed for:
- Accuracy
- Performance
- Testability
- Extensibility

All monetary values are rounded using
config-defined precision.
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP
from flask import current_app


class EMIEngine:
    """
    Enterprise-grade EMI calculation service.
    """

    @staticmethod
    def _round(value):
        """
        Centralized rounding using config precision.
        """
        precision = current_app.config.get("DECIMAL_PRECISION", 2)
        return float(
            Decimal(value).quantize(
                Decimal("1." + "0" * precision),
                rounding=ROUND_HALF_UP
            )
        )

    @staticmethod
    def validate_inputs(principal, annual_rate, tenure_months):
        """
        Validate loan parameters against system rules.
        """

        config = current_app.config

        if principal < config["MIN_LOAN_AMOUNT"]:
            raise ValueError("Loan amount below minimum allowed")

        if principal > config["MAX_LOAN_AMOUNT"]:
            raise ValueError("Loan amount exceeds maximum allowed")

        if annual_rate < 0 or annual_rate > config["MAX_INTEREST_RATE"]:
            raise ValueError("Invalid interest rate")

        if tenure_months <= 0 or tenure_months > config["MAX_TENURE_MONTHS"]:
            raise ValueError("Invalid tenure duration")

    @staticmethod
    def calculate(principal, annual_rate, tenure_months):
        """
        Calculate EMI and full loan metrics.
        """

        # Validate first
        EMIEngine.validate_inputs(principal, annual_rate, tenure_months)

        monthly_rate = annual_rate / (12 * 100)

        if monthly_rate == 0:
            emi = principal / tenure_months
        else:
            emi = (
                principal
                * monthly_rate
                * (1 + monthly_rate) ** tenure_months
            ) / ((1 + monthly_rate) ** tenure_months - 1)

        total_payment = emi * tenure_months
        total_interest = total_payment - principal

        # Effective annual rate (APR equivalent)
        effective_annual_rate = (
            (1 + monthly_rate) ** 12 - 1
        ) * 100 if monthly_rate > 0 else 0

        # Loan end date
        end_date = datetime.today() + relativedelta(months=tenure_months)

        return {
            "emi": EMIEngine._round(emi),
            "principal": EMIEngine._round(principal),
            "annual_interest_rate": EMIEngine._round(annual_rate),
            "monthly_interest_rate": EMIEngine._round(monthly_rate * 100),
            "total_interest": EMIEngine._round(total_interest),
            "total_payment": EMIEngine._round(total_payment),
            "effective_annual_rate": EMIEngine._round(effective_annual_rate),
            "tenure_months": tenure_months,
            "loan_end_date": end_date.strftime("%d %b %Y"),
        }