"""
Core Extensions Initialization
--------------------------------
Initializes all Flask extensions
in a centralized, scalable, production-safe way.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate


# ==============================
# DATABASE
# ==============================

db = SQLAlchemy(
    session_options={
        "autoflush": False,
        "expire_on_commit": False
    }
)


# ==============================
# LOGIN MANAGER
# ==============================

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"  # must match your auth blueprint
login_manager.login_message_category = "warning"


# ==============================
# CACHE SYSTEM
# ==============================

cache = Cache()


# ==============================
# RATE LIMITING
# ==============================

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


# ==============================
# MIGRATIONS
# ==============================

migrate = Migrate()


# ==============================
# EXTENSION INITIALIZER
# ==============================

def init_extensions(app):
    """
    Initialize all extensions with the app instance.
    """

    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # ==============================
    # USER LOADER (CRITICAL FIX)
    # ==============================
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    return app