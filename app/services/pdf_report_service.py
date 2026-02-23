"""
PDF Report Service
-------------------
Generates professional EMI loan report PDF.

Features:
- Clean bank-style layout
- EMI summary
- Amortization table
- Interest summary
- Branding footer
- Monetization CTA space
"""

import os
from datetime import datetime
from flask import current_app
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable
from reportlab.lib.styles import getSampleStyleSheet


class PDFReportService:

    @staticmethod
    def generate_report(calculation_result, amortization_schedule, filename="emi_report.pdf"):
        """
        Generate EMI PDF report.
        """

        file_path = os.path.join("reports", filename)

        if not os.path.exists("reports"):
            os.makedirs("reports")

        doc = SimpleDocTemplate(file_path)
        elements = []

        styles = getSampleStyleSheet()

        title_style = styles["Heading1"]
        normal_style = styles["Normal"]

        # ===========================
        # TITLE
        # ===========================
        elements.append(Paragraph("EMI Loan Report", title_style))
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(
            Paragraph(
                f"Generated on: {datetime.today().strftime('%d %b %Y')}",
                normal_style
            )
        )
        elements.append(Spacer(1, 0.3 * inch))

        # ===========================
        # SUMMARY TABLE
        # ===========================
        summary_data = [
            ["Loan Amount", f"{calculation_result['principal']}"],
            ["Interest Rate (%)", f"{calculation_result['annual_interest_rate']}"],
            ["Tenure (Months)", f"{calculation_result['tenure_months']}"],
            ["Monthly EMI", f"{calculation_result['emi']}"],
            ["Total Interest", f"{calculation_result['total_interest']}"],
            ["Total Payment", f"{calculation_result['total_payment']}"],
            ["Loan End Date", f"{calculation_result['loan_end_date']}"],
        ]

        summary_table = Table(summary_data, hAlign="LEFT")
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 0.5 * inch))

        # ===========================
        # AMORTIZATION TABLE (LIMIT FIRST 12 ROWS FOR PDF SIZE)
        # ===========================
        amortization_data = [
            ["Month", "EMI", "Principal", "Interest", "Balance"]
        ]

        for row in amortization_schedule[:12]:
            amortization_data.append([
                row["month"],
                row["emi"],
                row["principal_paid"],
                row["interest_paid"],
                row["remaining_balance"]
            ])

        amort_table = Table(amortization_data, repeatRows=1)
        amort_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
        ]))

        elements.append(Paragraph("Amortization Schedule (First 12 Months)", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(amort_table)

        elements.append(Spacer(1, 0.5 * inch))

        # ===========================
        # FOOTER CTA (Monetization Ready)
        # ===========================
        elements.append(
            Paragraph(
                "Looking for better loan rates? Compare offers today and save more.",
                styles["Italic"]
            )
        )

        doc.build(elements)

        return file_path