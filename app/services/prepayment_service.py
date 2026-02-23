"""
Prepayment Service
-------------------
Handles advanced loan simulations:

Features:
- Lump sum prepayment
- Monthly extra payment
- Tenure reduction calculation
- Interest savings calculation
- Before vs After comparison
- Graph-ready results
"""

from decimal import Decimal, ROUND_HALF_UP
from flask import current_app
from app.services.emi_engine import EMIEngine


class PrepaymentService:

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
    def simulate_lump_sum(principal, annual_rate, tenure_months, lump_sum, after_month):
        """
        Simulate one-time prepayment after specific month.
        """

        base = EMIEngine.calculate(principal, annual_rate, tenure_months)
        emi = base["emi"]
        monthly_rate = annual_rate / (12 * 100)

        balance = principal
        total_interest_paid = 0
        month = 0

        while balance > 0 and month < tenure_months:
            month += 1

            interest = balance * monthly_rate
            principal_component = emi - interest
            balance -= principal_component

            total_interest_paid += interest

            # Apply lump sum at specific month
            if month == after_month:
                balance -= lump_sum

            if balance <= 0:
                break

        new_tenure = month
        original_interest = base["total_interest"]
        interest_saved = original_interest - total_interest_paid

        return {
            "new_tenure_months": new_tenure,
            "interest_saved": PrepaymentService._round(interest_saved),
            "tenure_reduced": tenure_months - new_tenure,
        }

    @staticmethod
    def simulate_monthly_extra(principal, annual_rate, tenure_months, extra_monthly):
        """
        Simulate extra monthly payment.
        """

        base = EMIEngine.calculate(principal, annual_rate, tenure_months)
        emi = base["emi"]
        monthly_rate = annual_rate / (12 * 100)

        balance = principal
        total_interest_paid = 0
        month = 0

        while balance > 0:
            month += 1

            interest = balance * monthly_rate
            principal_component = emi - interest + extra_monthly
            balance -= principal_component

            total_interest_paid += interest

            if balance <= 0:
                break

        new_tenure = month
        original_interest = base["total_interest"]
        interest_saved = original_interest - total_interest_paid

        return {
            "new_tenure_months": new_tenure,
            "interest_saved": PrepaymentService._round(interest_saved),
            "tenure_reduced": tenure_months - new_tenure,
        }

    @staticmethod
    def comparison_summary(principal, annual_rate, tenure_months, extra_monthly):
        """
        Returns before vs after comparison summary.
        """

        base = EMIEngine.calculate(principal, annual_rate, tenure_months)
        extra = PrepaymentService.simulate_monthly_extra(
            principal, annual_rate, tenure_months, extra_monthly
        )

        return {
            "original_tenure": tenure_months,
            "new_tenure": extra["new_tenure_months"],
            "tenure_reduction": extra["tenure_reduced"],
            "original_interest": base["total_interest"],
            "interest_saved": extra["interest_saved"],
        }