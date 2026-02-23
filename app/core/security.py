"""
Security Layer
---------------
Applies secure headers and Content Security Policy (CSP)
for fintech-level protection.

Designed to:
- Prevent XSS
- Prevent Clickjacking
- Protect cookies
- Allow Google AdSense safely
"""

from flask import request


def apply_security_headers(app):
    """
    Attach secure headers globally.
    """

    @app.after_request
    def set_secure_headers(response):

        # ===============================
        # BASIC SECURITY HEADERS
        # ===============================
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # ===============================
        # STRICT TRANSPORT SECURITY
        # (Enable only in HTTPS production)
        # ===============================
        if not app.debug:
            response.headers["Strict-Transport-Security"] = \
                "max-age=31536000; includeSubDomains"

        # ===============================
        # CONTENT SECURITY POLICY
        # ===============================
        # Allow:
        # - Self resources
        # - Google AdSense
        # - Chart.js CDN
        # - Inline scripts (minimal, controlled)
        # - Google Fonts (if used later)

        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' https://pagead2.googlesyndication.com "
            "https://www.googletagmanager.com "
            "https://cdn.jsdelivr.net "
            "'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https://pagead2.googlesyndication.com; "
            "connect-src 'self'; "
            "frame-src https://googleads.g.doubleclick.net "
            "https://tpc.googlesyndication.com;"
        )

        response.headers["Content-Security-Policy"] = csp_policy

        # ===============================
        # REMOVE SERVER INFO
        # ===============================
        response.headers.pop("Server", None)

        return response