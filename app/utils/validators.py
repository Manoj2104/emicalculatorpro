"""
Validation Utilities
---------------------
Central validation logic for:

- EMI inputs
- Comparison inputs
- Prepayment inputs
- Auth inputs
"""

import re


# ===============================
# EMI INPUT VALIDATION
# ===============================
def validate_emi_inputs(principal, rate, tenure):
    if principal <= 0:
        return False, "Loan amount must be greater than zero."
    if rate < 0:
        return False, "Interest rate cannot be negative."
    if tenure <= 0:
        return False, "Tenure must be greater than zero."
    return True, None


# ===============================
# COMPARISON VALIDATION
# ===============================
def validate_comparison_loans(loans):
    if not isinstance(loans, list):
        return False, "Loans must be a list."

    if len(loans) < 2 or len(loans) > 3:
        return False, "Compare between 2 and 3 loans."

    for loan in loans:
        if loan["principal"] <= 0 or loan["tenure"] <= 0:
            return False, "Invalid loan values."

    return True, None


# ===============================
# PREPAYMENT VALIDATION
# ===============================
def validate_prepayment(principal, rate, tenure):
    if principal <= 0:
        return False, "Invalid principal."
    if rate < 0:
        return False, "Invalid interest rate."
    if tenure <= 0:
        return False, "Invalid tenure."
    return True, None


# ===============================
# EMAIL VALIDATION
# ===============================
def validate_email(email):
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(pattern, email) is not None


# ===============================
# PASSWORD STRENGTH CHECK
# ===============================
def validate_password_strength(password):
    if len(password) < 6:
        return False
    return True