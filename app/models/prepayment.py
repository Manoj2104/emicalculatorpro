"""
Prepayment Simulation Model
----------------------------
Stores prepayment simulation records.

Supports:
- Lump sum simulations
- Monthly extra simulations
- Savings tracking
- Dashboard analytics
- SQLite + PostgreSQL compatible
"""

from datetime import datetime
from sqlalchemy import JSON
from app.core.extensions import db


class PrepaymentSimulation(db.Model):
    __tablename__ = "prepayment_simulations"

    # ===============================
    # PRIMARY KEY
    # ===============================
    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # BASE LOAN DETAILS
    # ===============================
    principal = db.Column(db.Numeric(15, 2), nullable=False)
    annual_interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    tenure_months = db.Column(db.Integer, nullable=False)

    # ===============================
    # PREPAYMENT DETAILS
    # ===============================
    simulation_type = db.Column(
        db.String(20),
        nullable=False
    )  # lump_sum / monthly_extra

    # Portable JSON field (works in SQLite + PostgreSQL)
    prepayment_data = db.Column(
        JSON,
        nullable=True
    )

    # ===============================
    # SAVINGS SUMMARY
    # ===============================
    interest_saved = db.Column(db.Numeric(15, 2), nullable=False)
    tenure_reduced = db.Column(db.Integer, nullable=False)

    # ===============================
    # USER + IP
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
            "principal": float(self.principal),
            "rate": float(self.annual_interest_rate),
            "tenure_months": self.tenure_months,
            "simulation_type": self.simulation_type,
            "prepayment_data": self.prepayment_data,
            "interest_saved": float(self.interest_saved),
            "tenure_reduced": self.tenure_reduced,
            "created_at": self.created_at.strftime("%d %b %Y")
        }

    # ===============================
    # DEBUG REPRESENTATION
    # ===============================
    def __repr__(self):
        return f"<PrepaymentSimulation {self.id}>"