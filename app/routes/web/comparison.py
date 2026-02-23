"""
Comparison Web Routes
----------------------
Handles:

- Loan comparison page
- SEO injection
- Structured data
- Feature flag handling
"""

from flask import Blueprint, render_template, current_app
import json

comparison_bp = Blueprint("comparison", __name__)


@comparison_bp.route("/loan-comparison-calculator")
def loan_comparison_page():

    config = current_app.config

    # ===============================
    # SEO METADATA
    # ===============================
    seo_data = {
        "title": "Loan Comparison Calculator – Compare EMI & Save Money",
        "description": "Compare up to 3 loans side-by-side. Find the best EMI, lowest interest and smartest loan option.",
        "url": f"{config['SITE_URL']}/loan-comparison-calculator"
    }

    # ===============================
    # STRUCTURED DATA
    # ===============================
    structured_data = {
        "@context": "https://schema.org",
        "@type": "FinancialProduct",
        "name": "Loan Comparison Calculator",
        "description": seo_data["description"],
        "provider": {
            "@type": "Organization",
            "name": config["SITE_NAME"]
        }
    }

    # ===============================
    # FEATURE FLAGS
    # ===============================
    features = {
        "comparison": config["ENABLE_LOAN_COMPARISON"],
        "ads": config["ENABLE_ADS"]
    }

    return render_template(
        "comparison.html",
        seo=seo_data,
        structured_json=json.dumps(structured_data),
        features=features,
        max_loans=3,
        adsense_client=config["ADSENSE_CLIENT_ID"]
    )