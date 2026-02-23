"""
User Model
-----------
Handles:

- Authentication
- Subscription tier
- Role management
- Future SaaS expansion
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.core.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    # ===============================
    # PRIMARY KEY
    # ===============================
    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # AUTH FIELDS
    # ===============================
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # ===============================
    # PROFILE
    # ===============================
    role = db.Column(db.String(20), default="user")  # user / admin
    subscription_tier = db.Column(db.String(20), default="free")  # free / pro
    is_active = db.Column(db.Boolean, default=True)

    # ===============================
    # METADATA
    # ===============================
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ===============================
    # PASSWORD METHODS
    # ===============================
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ===============================
    # SERIALIZE
    # ===============================
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "subscription_tier": self.subscription_tier,
            "created_at": self.created_at.strftime("%d %b %Y")
        }

    def __repr__(self):
        return f"<User {self.email}>"