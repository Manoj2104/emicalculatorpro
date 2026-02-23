"""
Loan Comparison Service
------------------------
Compares multiple loan options intelligently.

Features:
- Compare up to 3 loans
- EMI comparison
- Total interest comparison
- Cost efficiency score
- Automatic best loan ranking
"""

from decimal import Decimal, ROUND_HALF_UP
from flask import current_app
from app.services.emi_engine import EMIEngine


class LoanComparisonService:

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
    def compare(loans):
        """
        loans = [
            {"principal": 1000000, "rate": 8.5, "tenure": 240},
            {"principal": 1000000, "rate": 8.2, "tenure": 240},
        ]
        """

        if len(loans) < 2 or len(loans) > 3:
            raise ValueError("You can compare between 2 and 3 loans only.")

        results = []

        for idx, loan in enumerate(loans):
            calc = EMIEngine.calculate(
                loan["principal"],
                loan["rate"],
                loan["tenure"]
            )

            efficiency_score = LoanComparisonService._calculate_efficiency_score(calc)

            results.append({
                "loan_id": idx + 1,
                "principal": calc["principal"],
                "rate": calc["annual_interest_rate"],
                "tenure": calc["tenure_months"],
                "emi": calc["emi"],
                "total_interest": calc["total_interest"],
                "total_payment": calc["total_payment"],
                "efficiency_score": efficiency_score
            })

        # Sort by total payment (lowest is best)
        ranked = sorted(results, key=lambda x: x["total_payment"])

        # Mark best loan
        ranked[0]["best_option"] = True
        for r in ranked[1:]:
            r["best_option"] = False

        return ranked

    @staticmethod
    def _calculate_efficiency_score(calculation_result):
        """
        Custom financial efficiency score.
        Lower total payment → higher score.
        """

        total_payment = calculation_result["total_payment"]
        principal = calculation_result["principal"]

        # Efficiency formula (custom scoring logic)
        cost_ratio = total_payment / principal
        score = 100 - ((cost_ratio - 1) * 100)

        return LoanComparisonService._round(max(score, 0))