# -*- coding: utf-8 -*-
"""
ZATCA Settings Page
"""

import frappe
from frappe import _

def get_context(context):
    """Get context for ZATCA Settings page"""
    context.title = _("ZATCA Settings")
    context.breadcrumbs = [
        {"label": _("Home"), "route": "/"},
        {"label": _("ZATCA Settings"), "route": "/app/zatca-settings"}
    ]
    
    # Get or create ZATCA Settings
    if not frappe.db.exists("ZATCA Settings", "Default"):
        frappe.get_doc({
            'doctype': 'ZATCA Settings',
            'name': 'Default',
            'vat_number': '',
            'company_name': '',
            'api_key': '',
            'secret_key': '',
            'test_mode': 1,
            'base_url': 'https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal'
        }).insert()
    
    settings = frappe.get_doc("ZATCA Settings", "Default")
    context.settings = settings 