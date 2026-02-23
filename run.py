"""
Application Entry Point
------------------------
Used for:

- Local development
- Debug mode
- CLI access
- Running Flask app directly

For production:
Use wsgi.py with Gunicorn
"""

import os
from dotenv import load_dotenv
from app import create_app

# ===============================
# LOAD ENV VARIABLES
# ===============================
load_dotenv()

# ===============================
# CREATE APP INSTANCE
# ===============================
app = create_app()


# ===============================
# SHELL CONTEXT (Flask CLI)
# ===============================
@app.shell_context_processor
def make_shell_context():
    from app.core.extensions import db
    from app.models.user import User
    from app.models.calculation import Calculation
    from app.models.loan_comparison import LoanComparison
    from app.models.prepayment import PrepaymentSimulation

    return {
        "db": db,
        "User": User,
        "Calculation": Calculation,
        "LoanComparison": LoanComparison,
        "PrepaymentSimulation": PrepaymentSimulation
    }


# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":

    debug_mode = os.getenv("FLASK_DEBUG", "False") == "True"
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))

    app.run(
        host=host,
        port=port,
        debug=debug_mode
    )