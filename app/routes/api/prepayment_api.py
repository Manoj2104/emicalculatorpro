"""
Prepayment API Route
---------------------
Handles:

POST /api/prepayment

Supports:
- Lump sum prepayment
- Monthly extra payment
- Returns interest savings
- Returns tenure reduction
"""

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from app.core.extensions import db, limiter
from app.models.calculation import Calculation
from app.services.prepayment_service import PrepaymentService
from app.services.emi_engine import EMIEngine

prepayment_api_bp = Blueprint("prepayment_api", __name__)


@prepayment_api_bp.route("/prepayment", methods=["POST"])
@limiter.limit("20 per minute")
def simulate_prepayment():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON input"}), 400

        principal = float(data.get("principal", 0))
        rate = float(data.get("rate", 0))
        tenure = int(data.get("tenure", 0))

        lump_sum = float(data.get("lump_sum", 0))
        after_month = int(data.get("after_month", 0))
        extra_monthly = float(data.get("extra_monthly", 0))

        # Validate basic EMI first
        base_calculation = EMIEngine.calculate(principal, rate, tenure)

        # ===============================
        # LUMP SUM SIMULATION
        # ===============================
        if lump_sum > 0 and after_month > 0:
            result = PrepaymentService.simulate_lump_sum(
                principal,
                rate,
                tenure,
                lump_sum,
                after_month
            )

        # ===============================
        # MONTHLY EXTRA SIMULATION
        # ===============================
        elif extra_monthly > 0:
            result = PrepaymentService.simulate_monthly_extra(
                principal,
                rate,
                tenure,
                extra_monthly
            )

        else:
            return jsonify({
                "error": "Provide lump_sum + after_month OR extra_monthly"
            }), 400

        # ===============================
        # SAVE PREPAYMENT RECORD
        # ===============================
        record = Calculation(
            principal=principal,
            annual_interest_rate=rate,
            tenure_months=tenure,
            emi=base_calculation["emi"],
            total_interest=base_calculation["total_interest"],
            total_payment=base_calculation["total_payment"],
            currency="USD",
            prepayment_used=True,
            prepayment_data=result,
            ip_address=request.remote_addr
        )

        db.session.add(record)
        db.session.commit()

        # ===============================
        # RESPONSE
        # ===============================
        return jsonify({
            "original": base_calculation,
            "prepayment_result": result
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        current_app.logger.error(f"Prepayment API Error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500