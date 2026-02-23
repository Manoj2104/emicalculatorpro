"""
Application Factory
---------------------
Creates and configures the Flask app instance.

Why App Factory?
- Supports multiple environments
- Enables testing
- Prevents circular imports
- Scales cleanly
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify

from config import config_by_name
from app.core.extensions import init_extensions
from app.core.security import apply_security_headers


# ==========================================
# CREATE APPLICATION
# ==========================================

def create_app(config_name=None):
    """
    Application factory function.
    """

    # Determine environment
    env = config_name or os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_by_name[env])

    # Initialize Extensions
    init_extensions(app)

    # Apply security headers
    apply_security_headers(app)

    # Register Blueprints
    register_blueprints(app)

    # Register Error Handlers
    register_error_handlers(app)

    # Setup Logging (Production Safe)
    configure_logging(app)

    return app


# ==========================================
# BLUEPRINT REGISTRATION
# ==========================================

def register_blueprints(app):
    """
    Register all application blueprints.
    """

    from app.routes.web.main import web_main_bp
    from app.routes.web.calculator import calculator_bp
    from app.routes.web.comparison import comparison_bp
    from app.routes.web.reports import reports_bp

    from app.routes.api.emi_api import emi_api_bp
    from app.routes.api.prepayment_api import prepayment_api_bp
    from app.routes.api.comparison_api import comparison_api_bp
    from app.routes.api.history_api import history_api_bp
    from app.core.caching import init_cache
    
    init_cache(app)
    # Web routes
    app.register_blueprint(web_main_bp)
    app.register_blueprint(calculator_bp)
    app.register_blueprint(comparison_bp)
    app.register_blueprint(reports_bp)
    

    # API routes
    app.register_blueprint(emi_api_bp, url_prefix="/api")
    app.register_blueprint(prepayment_api_bp, url_prefix="/api")
    app.register_blueprint(comparison_api_bp, url_prefix="/api")
    app.register_blueprint(history_api_bp, url_prefix="/api")


# ==========================================
# ERROR HANDLERS
# ==========================================

def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource Not Found"}), 404

    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({"error": "Too many requests. Please slow down."}), 429

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Internal Server Error"}), 500


# ==========================================
# LOGGING CONFIGURATION
# ==========================================

def configure_logging(app):
    """
    Production-grade rotating file logging.
    """

    if not app.debug:

        if not os.path.exists("logs"):
            os.mkdir("logs")

        file_handler = RotatingFileHandler(
            "logs/emi_app.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )

        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ))

        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("EMI Calculator Pro startup")