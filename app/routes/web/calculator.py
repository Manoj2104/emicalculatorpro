"""
Calculator Web Routes
----------------------
Handles:

- Main calculator page
- Loan-type specific pages
- SEO optimized URLs
"""

from flask import Blueprint, render_template, current_app
from app.services.currency_service import CurrencyService

# IMPORTANT: Add url_prefix
calculator_bp = Blueprint(
    "calculator",
    __name__,
    url_prefix="/calculator"
)


# ===============================
# DEFAULT CALCULATOR PAGE
# ===============================
@calculator_bp.route("/")
def calculator_home():

    config = current_app.config

    seo_data = {
        "title": "Loan EMI Calculator – Calculate EMI Instantly",
        "description": "Calculate your loan EMI with amortization schedule, prepayment simulation, and comparison tools.",
        "url": f"{config['SITE_URL']}/calculator"
    }

    return render_template(
        "calculator.html",
        seo=seo_data,
        currencies=CurrencyService.supported_currencies(),
        features={
            "pdf": config.get("ENABLE_PDF_EXPORT", False),
            "comparison": config.get("ENABLE_LOAN_COMPARISON", False),
            "prepayment": config.get("ENABLE_PREPAYMENT_SIMULATOR", False),
            "currency": config.get("ENABLE_CURRENCY_CONVERSION", False),
            "ads": config.get("ENABLE_ADS", False)
        },
        adsense_client=config.get("ADSENSE_CLIENT_ID")
    )


# ===============================
# LOAN TYPE SPECIFIC PAGES
# ===============================
@calculator_bp.route("/<loan_type>-loan-emi-calculator")
def loan_type_calculator(loan_type):

    config = current_app.config

    allowed_types = [
        "home",
        "car",
        "personal",
        "education",
        "business"
    ]

    if loan_type not in allowed_types:
        return render_template("404.html"), 404

    seo_data = {
        "title": f"{loan_type.capitalize()} Loan EMI Calculator – Accurate & Fast",
        "description": f"Calculate your {loan_type} loan EMI with detailed amortization schedule and prepayment simulation.",
        "url": f"{config['SITE_URL']}/{loan_type}-loan-emi-calculator"
    }

    return render_template(
        "calculator.html",
        seo=seo_data,
        loan_type=loan_type,
        currencies=CurrencyService.supported_currencies(),
        features={
            "pdf": config.get("ENABLE_PDF_EXPORT", False),
            "comparison": config.get("ENABLE_LOAN_COMPARISON", False),
            "prepayment": config.get("ENABLE_PREPAYMENT_SIMULATOR", False),
            "currency": config.get("ENABLE_CURRENCY_CONVERSION", False),
            "ads": config.get("ENABLE_ADS", False)
        },
        adsense_client=config.get("ADSENSE_CLIENT_ID")
    )

@calculator_bp.route("/home-loan-eligibility")
def home_loan_eligibility():
    return render_template("home_loan_eligibility.html")

@calculator_bp.route("/loan-eligibility-by-salary")
def loan_eligibility_salary():
    return render_template("loan_eligibility_salary.html")

@calculator_bp.route("/prepayment-calculator")
def prepayment_calculator():
    return render_template("prepayment_calculator.html")

@calculator_bp.route("/sip-calculator")
def sip_calculator():
    return render_template("sip_calculator.html", seo={
        "title": "SIP Calculator | EMI Calculator Pro"
    })

@calculator_bp.route("/lumpsum-calculator")
def lumpsum_calculator():
    return render_template("lumpsum-calculator.html")

@calculator_bp.route("/retirement-calculator")
def retirement_calculator():
    return render_template("retirement_calculator.html")

@calculator_bp.route("/inflation-calculator")
def inflation_calculator():
    return render_template("inflation_calculator.html")

@calculator_bp.route("/dti-calculator")
def dti_calculator():
    return render_template("dti_calculator.html")

@calculator_bp.route("/credit-card-emi")
def credit_card_emi():
    return render_template("credit_card_emi.html")

@calculator_bp.route("/gst-calculator")
def gst_calculator():
    return render_template("gst_calculator.html")

@calculator_bp.route("/compound-interest-calculator")
def compound_interest_calculator():
    return render_template("compound_interest.html")

@calculator_bp.route("/fd-calculator")
def fd_calculator():
    return render_template("fd_calculator.html")

@calculator_bp.route("/rd-calculator")
def rd_calculator():
    return render_template("rd_calculator.html")