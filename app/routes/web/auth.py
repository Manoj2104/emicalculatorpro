"""
Authentication Routes
----------------------
Handles:

- User Registration
- User Login
- Logout
- Session management
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app.core.extensions import db, limiter, login_manager
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


# ===============================
# USER LOADER (Flask-Login)
# ===============================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ===============================
# REGISTER
# ===============================
@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():

    if current_user.is_authenticated:
        return redirect(url_for("web_main.home"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please fill all fields.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "warning")
            return redirect(url_for("auth.register"))

        try:
            user = User(email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash("Account created successfully. Please login.", "success")
            return redirect(url_for("auth.login"))

        except SQLAlchemyError:
            db.session.rollback()
            flash("Database error occurred.", "danger")
            return redirect(url_for("auth.register"))

    return render_template("auth/register.html")


# ===============================
# LOGIN
# ===============================
@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():

    if current_user.is_authenticated:
        return redirect(url_for("web_main.home"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            flash("Login successful.", "success")
            return redirect(url_for("dashboard.dashboard_home"))

        flash("Invalid email or password.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


# ===============================
# LOGOUT
# ===============================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("web_main.home"))