"""
Comparison API Route
---------------------
Handles:

POST /api/compare-loans

Accepts:
{
    "loans": [
        {"principal": 1000000, "rate": 8.5, "tenure": 240},
        {"principal": 1000000, "rate": 8.2, "tenure": 240}
    ]
}

Returns ranked comparison result.
"""

import uuid
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from app.core.extensions import db, limiter
from app.models.calculation import Calculation
from app.services.comparison_service import LoanComparisonService

comparison_api_bp = Blueprint("comparison_api", __name__)


@comparison_api_bp.route("/compare-loans", methods=["POST"])
@limiter.limit("15 per minute")
def compare_loans():
    try:
        data = request.get_json()

        if not data or "loans" not in data:
            return jsonify({"error": "Missing loans data"}), 400

        loans = data["loans"]

        if not isinstance(loans, list):
            return jsonify({"error": "Loans must be a list"}), 400

        if len(loans) < 2 or len(loans) > 3:
            return jsonify({"error": "Compare between 2 and 3 loans only"}), 400

        # ===============================
        # RUN COMPARISON ENGINE
        # ===============================
        results = LoanComparisonService.compare(loans)

        # ===============================
        # CREATE GROUP ID
        # ===============================
        comparison_group_id = str(uuid.uuid4())

        # ===============================
        # SAVE EACH LOAN RECORD
        # ===============================
        for r in results:
            record = Calculation(
                principal=r["principal"],
                annual_interest_rate=r["rate"],
                tenure_months=r["tenure"],
                emi=r["emi"],
                total_interest=r["total_interest"],
                total_payment=r["total_payment"],
                currency="USD",
                comparison_group_id=comparison_group_id,
                ip_address=request.remote_addr
            )

            db.session.add(record)

        db.session.commit()

        # ===============================
        # RESPONSE
        # ===============================
        return jsonify({
            "comparison_group_id": comparison_group_id,
            "results": results
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        current_app.logger.error(f"Comparison API Error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500