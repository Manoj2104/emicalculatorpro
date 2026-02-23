import os
import logging   # ✅ THIS WAS MISSING
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create app instance
app = create_app()

# Optional: Attach Gunicorn logging in production
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    if gunicorn_logger.handlers:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)