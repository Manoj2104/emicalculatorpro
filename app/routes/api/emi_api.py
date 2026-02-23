"""
EMI API Route
--------------
Handles:

POST /api/calculate-emi

Responsibilities:
- Validate inputs
- Perform EMI calculation
- Generate amortization schedule
- Optional currency conversion
- Save to database
- Return structured JSON
"""

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from app.core.extensions import db, limiter
from app.models.calculation import Calculation
from app.services.emi_engine import EMIEngine
from app.services.amortization_service import AmortizationService
from app.services.currency_service import CurrencyService

emi_api_bp = Blueprint("emi_api", __name__)


@emi_api_bp.route("/calculate-emi", methods=["POST"])
@limiter.limit("20 per minute")
def calculate_emi():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON input"}), 400

        principal = float(data.get("principal", 0))
        rate = float(data.get("rate", 0))
        tenure = int(data.get("tenure", 0))
        currency = data.get("currency", "USD")

        # ===============================
        # EMI CALCULATION
        # ===============================
        calculation = EMIEngine.calculate(principal, rate, tenure)

        # ===============================
        # AMORTIZATION
        # ===============================
        schedule = AmortizationService.generate_schedule(
            principal, rate, tenure
        )

        yearly_summary = AmortizationService.generate_yearly_summary(schedule)

        graph_data = AmortizationService.graph_data(schedule)

        # ===============================
        # CURRENCY CONVERSION
        # ===============================
        if currency != "USD":
            conversion = CurrencyService.convert(
                calculation["emi"], "USD", currency
            )
            calculation["emi_converted"] = conversion["converted_amount"]
            calculation["currency"] = currency
        else:
            calculation["currency"] = "USD"

        # ===============================
        # SAVE TO DATABASE
        # ===============================
        record = Calculation(
            principal=principal,
            annual_interest_rate=rate,
            tenure_months=tenure,
            emi=calculation["emi"],
            total_interest=calculation["total_interest"],
            total_payment=calculation["total_payment"],
            currency=calculation["currency"],
            ip_address=request.remote_addr
        )

        db.session.add(record)
        db.session.commit()

        # ===============================
        # RESPONSE
        # ===============================
        return jsonify({
            "calculation": calculation,
            "amortization": schedule,
            "yearly_summary": yearly_summary,
            "graph_data": graph_data
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        current_app.logger.error(f"EMI API Error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500