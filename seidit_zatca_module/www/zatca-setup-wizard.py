# -*- coding: utf-8 -*-
"""
ZATCA Setup Wizard Page
"""

import frappe
from frappe import _

def get_context(context):
    """Get context for ZATCA Setup Wizard page"""
    context.title = _("ZATCA Setup Wizard")
    context.breadcrumbs = [
        {"label": _("Home"), "route": "/"},
        {"label": _("ZATCA Setup Wizard"), "route": "/app/zatca-setup-wizard"}
    ]
    
    # Get or create ZATCA Setup Wizard
    if not frappe.db.exists("ZATCA Setup Wizard", "Default"):
        frappe.get_doc({
            'doctype': 'ZATCA Setup Wizard',
            'name': 'Default',
            'step': 'Welcome',
            'vat_number': '',
            'company_name': '',
            'api_key': '',
            'secret_key': '',
            'test_mode': 1,
            'installation_id': frappe.generate_hash(length=16)
        }).insert()
    
    wizard = frappe.get_doc("ZATCA Setup Wizard", "Default")
    context.wizard = wizard
    context.steps = [
        "Welcome",
        "VAT Registration", 
        "ZATCA Portal Access",
        "API Credentials",
        "Test Connection",
        "Live Activation",
        "Invoice Testing",
        "License Warning",
        "Completion"
    ] 