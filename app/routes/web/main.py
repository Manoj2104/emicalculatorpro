"""
Main Web Routes
---------------
Handles:

- Home page
- SEO injection
- Structured data
- Feature flag exposure
"""

from flask import Blueprint, render_template, current_app, request
import json

web_main_bp = Blueprint("web_main", __name__)


@web_main_bp.route("/")
def home():
    """
    Render EMI Calculator homepage.
    """

    config = current_app.config

    # ===============================
    # SEO Metadata
    # ===============================
    seo_data = {
        "title": "EMI Calculator – Advanced Loan EMI & Prepayment Tool",
        "description": config["DEFAULT_META_DESCRIPTION"],
        "url": config["SITE_URL"],
    }

    # ===============================
    # Schema.org Structured Data
    # ===============================
    structured_data = {
        "@context": "https://schema.org",
        "@type": "FinancialProduct",
        "name": "EMI Calculator Pro",
        "description": config["DEFAULT_META_DESCRIPTION"],
        "url": config["SITE_URL"],
        "provider": {
            "@type": "Organization",
            "name": config["SITE_NAME"]
        }
    }

    # ===============================
    # Feature Flags
    # ===============================
    features = {
        "pdf": config["ENABLE_PDF_EXPORT"],
        "comparison": config["ENABLE_LOAN_COMPARISON"],
        "prepayment": config["ENABLE_PREPAYMENT_SIMULATOR"],
        "currency": config["ENABLE_CURRENCY_CONVERSION"],
        "ads": config["ENABLE_ADS"]
    }

    return render_template(
        "index.html",
        seo=seo_data,
        structured_json=json.dumps(structured_data),
        features=features,
        adsense_client=config["ADSENSE_CLIENT_ID"]
    )