"""
History API Route
------------------
Handles:

GET /api/history

Features:
- Pagination
- Filter by IP
- Filter by comparison group
- Performance optimized
- Ordered by latest first
"""

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from app.core.extensions import db, limiter
from app.models.calculation import Calculation

history_api_bp = Blueprint("history_api", __name__)


@history_api_bp.route("/history", methods=["GET"])
@limiter.limit("30 per minute")
def get_history():
    try:
        # ===============================
        # QUERY PARAMETERS
        # ===============================
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        ip_filter = request.args.get("ip")
        comparison_group = request.args.get("group_id")

        if per_page > 50:
            per_page = 50  # safety cap

        query = Calculation.query

        # ===============================
        # OPTIONAL FILTERS
        # ===============================
        if ip_filter:
            query = query.filter(Calculation.ip_address == ip_filter)

        if comparison_group:
            query = query.filter(
                Calculation.comparison_group_id == comparison_group
            )

        # ===============================
        # ORDER + PAGINATION
        # ===============================
        query = query.order_by(Calculation.created_at.desc())

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        results = [record.to_dict() for record in pagination.items]

        return jsonify({
            "page": page,
            "per_page": per_page,
            "total_records": pagination.total,
            "total_pages": pagination.pages,
            "results": results
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid pagination values"}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        current_app.logger.error(f"History API Error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500