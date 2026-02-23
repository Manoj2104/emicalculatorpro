"""
Reports Web Routes
-------------------
Handles:

- PDF report generation
- Secure file download
- Validation of calculation ID
"""

import os
from flask import Blueprint, send_file, abort, current_app
from sqlalchemy.exc import SQLAlchemyError

from app.models.calculation import Calculation
from app.services.amortization_service import AmortizationService
from app.services.pdf_report_service import PDFReportService
from app.services.emi_engine import EMIEngine

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/download-report/<int:calculation_id>")
def download_report(calculation_id):
    try:
        # ===============================
        # FETCH RECORD
        # ===============================
        record = Calculation.query.get(calculation_id)

        if not record:
            abort(404)

        # ===============================
        # REGENERATE CALCULATION
        # (Ensures data integrity)
        # ===============================
        calculation_result = EMIEngine.calculate(
            float(record.principal),
            float(record.annual_interest_rate),
            record.tenure_months
        )

        schedule = AmortizationService.generate_schedule(
            float(record.principal),
            float(record.annual_interest_rate),
            record.tenure_months
        )

        # ===============================
        # GENERATE PDF
        # ===============================
        filename = f"emi_report_{calculation_id}.pdf"

        file_path = PDFReportService.generate_report(
            calculation_result,
            schedule,
            filename=filename
        )

        # ===============================
        # SECURITY CHECK
        # ===============================
        if not os.path.exists(file_path):
            abort(404)

        # ===============================
        # SEND FILE
        # ===============================
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype="application/pdf"
        )

    except SQLAlchemyError:
        return abort(500)

    except Exception as e:
        current_app.logger.error(f"Report Download Error: {str(e)}")
        return abort(500)