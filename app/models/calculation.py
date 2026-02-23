"""
Calculation Model
------------------
Stores EMI calculations for:

- History tracking
- User saved reports
- Analytics
- Future SaaS subscriptions
- Loan comparison logging
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from app.core.extensions import db


class Calculation(db.Model):
    __tablename__ = "calculations"

    # ===============================
    # PRIMARY KEY
    # ===============================
    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # LOAN DETAILS
    # ===============================
    principal = db.Column(db.Numeric(15, 2), nullable=False)
    annual_interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    tenure_months = db.Column(db.Integer, nullable=False)

    emi = db.Column(db.Numeric(15, 2), nullable=False)
    total_interest = db.Column(db.Numeric(15, 2), nullable=False)
    total_payment = db.Column(db.Numeric(15, 2), nullable=False)

    # ===============================
    # OPTIONAL FEATURES
    # ===============================
    currency = db.Column(db.String(10), default="USD")

    prepayment_used = db.Column(db.Boolean, default=False)
    prepayment_data = db.Column(JSON, nullable=True)

    comparison_group_id = db.Column(db.String(50), nullable=True)

    # ===============================
    # USER TRACKING
    # ===============================
    user_id = db.Column(db.Integer, nullable=True, index=True)

    ip_address = db.Column(db.String(45), nullable=True)

    # ===============================
    # METADATA
    # ===============================
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # ===============================
    # INDEXES (Performance Boost)
    # ===============================
    __table_args__ = (
        db.Index("idx_principal_rate", "principal", "annual_interest_rate"),
        db.Index("idx_created_at", "created_at"),
    )

    # ===============================
    # SERIALIZATION METHOD
    # ===============================
    def to_dict(self):
        return {
            "id": self.id,
            "principal": float(self.principal),
            "annual_interest_rate": float(self.annual_interest_rate),
            "tenure_months": self.tenure_months,
            "emi": float(self.emi),
            "total_interest": float(self.total_interest),
            "total_payment": float(self.total_payment),
            "currency": self.currency,
            "prepayment_used": self.prepayment_used,
            "created_at": self.created_at.strftime("%d %b %Y"),
        }

    def __repr__(self):
        return f"<Calculation {self.id} | EMI {self.emi}>"