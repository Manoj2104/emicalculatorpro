"""
SEO Utilities
--------------
Handles:

- Dynamic title building
- OpenGraph tags
- Canonical links
- Structured data builder
"""

from flask import current_app


def build_meta(title, description, path=""):
    base_url = current_app.config.get("SITE_URL")

    return {
        "title": title,
        "description": description,
        "url": f"{base_url}{path}"
    }


def build_og_tags(title, description, url):
    return {
        "og:title": title,
        "og:description": description,
        "og:url": url,
        "og:type": "website"
    }


def build_structured_financial_product(name, description):
    return {
        "@context": "https://schema.org",
        "@type": "FinancialProduct",
        "name": name,
        "description": description,
        "provider": {
            "@type": "Organization",
            "name": current_app.config.get("SITE_NAME")
        }
    }