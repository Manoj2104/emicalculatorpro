import os
from datetime import timedelta


class BaseConfig:
    """
    Base configuration shared across all environments.
    """

    # ==============================
    # CORE SECURITY
    # ==============================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set True in production (HTTPS)
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # ==============================
    # DATABASE
    # ==============================
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    # Default fallback database (important for flask db commands)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///emi_dev.db"
    )

    # ==============================
    # CACHING
    # ==============================
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = 300

    # Optional Redis (production scaling)
    CACHE_REDIS_URL = os.getenv("REDIS_URL")

    # ==============================
    # RATE LIMITING
    # ==============================
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")

    # ==============================
    # EMI LIMITS
    # ==============================
    MAX_LOAN_AMOUNT = 100_000_000
    MIN_LOAN_AMOUNT = 1_000
    MAX_TENURE_MONTHS = 600
    MAX_INTEREST_RATE = 50
    DECIMAL_PRECISION = 2

    # ==============================
    # FEATURE FLAGS
    # ==============================
    ENABLE_PDF_EXPORT = True
    ENABLE_LOAN_COMPARISON = True
    ENABLE_PREPAYMENT_SIMULATOR = True
    ENABLE_CURRENCY_CONVERSION = True
    ENABLE_ADS = True

    # ==============================
    # GOOGLE ADS CONFIG
    # ==============================
    ADSENSE_CLIENT_ID = os.getenv("ADSENSE_CLIENT_ID", "")
    ADSENSE_TOP_SLOT = os.getenv("ADSENSE_TOP_SLOT", "")
    ADSENSE_INCONTENT_SLOT = os.getenv("ADSENSE_INCONTENT_SLOT", "")
    ADSENSE_SIDEBAR_SLOT = os.getenv("ADSENSE_SIDEBAR_SLOT", "")

    # ==============================
    # SECURITY HEADERS
    # ==============================
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "no-referrer-when-downgrade",
    }

    # ==============================
    # SEO
    # ==============================
    SITE_NAME = "EMI Calculator Pro"
    SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:5000")
    DEFAULT_META_DESCRIPTION = (
        "Advanced EMI Calculator with amortization, "
        "prepayment simulation and loan comparison."
    )


# ==============================
# DEVELOPMENT CONFIG
# ==============================
class DevelopmentConfig(BaseConfig):
    DEBUG = True


# ==============================
# PRODUCTION CONFIG
# ==============================
class ProductionConfig(BaseConfig):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    # Production MUST have DATABASE_URL set
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")


# ==============================
# CONFIG SELECTOR
# ==============================
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}


# Default fallback
def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)