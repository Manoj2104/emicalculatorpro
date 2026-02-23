"""
Amortization Service
---------------------
Generates detailed repayment schedule.

Features:
- Monthly breakdown
- Yearly aggregation
- Graph-ready data
- Safe balance handling
- Supports zero-interest loans
"""

from decimal import Decimal, ROUND_HALF_UP
from flask import current_app
from app.services.emi_engine import EMIEngine


class AmortizationService:

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
    def generate_schedule(principal, annual_rate, tenure_months):
        """
        Generate full amortization schedule.
        """

        result = EMIEngine.calculate(principal, annual_rate, tenure_months)

        emi = result["emi"]
        monthly_rate = annual_rate / (12 * 100)

        balance = principal
        schedule = []

        for month in range(1, tenure_months + 1):

            if monthly_rate == 0:
                interest = 0
                principal_component = emi
            else:
                interest = balance * monthly_rate
                principal_component = emi - interest

            # Prevent negative balance in final month
            if principal_component > balance:
                principal_component = balance
                emi = principal_component + interest

            balance -= principal_component

            schedule.append({
                "month": month,
                "emi": AmortizationService._round(emi),
                "principal_paid": AmortizationService._round(principal_component),
                "interest_paid": AmortizationService._round(interest),
                "remaining_balance": AmortizationService._round(max(balance, 0))
            })

            if balance <= 0:
                break

        return schedule

    @staticmethod
    def generate_yearly_summary(schedule):
        """
        Aggregate monthly schedule into yearly data.
        """

        yearly = {}
        for row in schedule:
            year = (row["month"] - 1) // 12 + 1

            if year not in yearly:
                yearly[year] = {
                    "year": year,
                    "total_principal": 0,
                    "total_interest": 0,
                    "total_payment": 0
                }

            yearly[year]["total_principal"] += row["principal_paid"]
            yearly[year]["total_interest"] += row["interest_paid"]
            yearly[year]["total_payment"] += row["emi"]

        # Round final values
        for year in yearly:
            yearly[year]["total_principal"] = AmortizationService._round(
                yearly[year]["total_principal"]
            )
            yearly[year]["total_interest"] = AmortizationService._round(
                yearly[year]["total_interest"]
            )
            yearly[year]["total_payment"] = AmortizationService._round(
                yearly[year]["total_payment"]
            )

        return list(yearly.values())

    @staticmethod
    def graph_data(schedule):
        """
        Prepare data for charts.
        """

        labels = []
        principal_data = []
        interest_data = []
        balance_data = []

        for row in schedule:
            labels.append(f"M{row['month']}")
            principal_data.append(row["principal_paid"])
            interest_data.append(row["interest_paid"])
            balance_data.append(row["remaining_balance"])

        return {
            "labels": labels,
            "principal": principal_data,
            "interest": interest_data,
            "balance": balance_data
        }