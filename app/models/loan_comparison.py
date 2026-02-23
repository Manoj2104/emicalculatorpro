"""
Loan Comparison Model
----------------------
Stores structured loan comparison sessions.

Supports:
- Up to 3 loans per comparison
- User tracking
- IP tracking
- Analytics-ready structure
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from app.core.extensions import db


class LoanComparison(db.Model):
    __tablename__ = "loan_comparisons"

    # ===============================
    # PRIMARY KEY
    # ===============================
    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # COMPARISON GROUP ID
    # ===============================
    comparison_group_id = db.Column(
        db.String(64),
        nullable=False,
        index=True
    )

    # ===============================
    # STORED LOANS DATA (JSON)
    # ===============================
    loans_data = db.Column(
        JSON,
        nullable=False
    )

    # ===============================
    # BEST LOAN RESULT
    # ===============================
    best_loan_id = db.Column(db.Integer, nullable=True)

    # ===============================
    # USER + IP TRACKING
    # ===============================
    user_id = db.Column(db.Integer, nullable=True, index=True)
    ip_address = db.Column(db.String(45), nullable=True)

    # ===============================
    # METADATA
    # ===============================
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        index=True
    )

    # ===============================
    # SERIALIZER
    # ===============================
    def to_dict(self):
        return {
            "id": self.id,
            "comparison_group_id": self.comparison_group_id,
            "loans_data": self.loans_data,
            "best_loan_id": self.best_loan_id,
            "created_at": self.created_at.strftime("%d %b %Y")
        }

    def __repr__(self):
        return f"<LoanComparison {self.comparison_group_id}>"