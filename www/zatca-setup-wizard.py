"""
ZATCA Setup Wizard Page Controller
==================================

Controller for the ZATCA Setup Wizard page.

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.
"""

import frappe

def get_context(context):
    """Get context for the ZATCA Setup Wizard page"""
    context.title = "ZATCA Setup Wizard"
    context.breadcrumbs = [
        {"label": "Home", "url": "/"},
        {"label": "ZATCA Setup Wizard", "url": "/zatca-setup-wizard"}
    ]
    
    # Add any additional context data
    context.provider = "SEIDiT"
    context.version = "2.0.0"
    context.support_email = "support@seidit.com"
    context.support_whatsapp = "+966567414356"
    
    return context 