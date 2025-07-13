#!/usr/bin/env python3
"""
ZATCA Phase 2 Module Installation Script for ERPNext
"""

import frappe
import os
import json

def install_zatca_module():
    """Install ZATCA Phase 2 module in ERPNext"""
    
    print("Installing ZATCA Phase 2 Module...")
    
    # Create ZATCA module
    if not frappe.db.exists("Module Def", "ZATCA"):
        frappe.get_doc({
            'doctype': 'Module Def',
            'module_name': 'ZATCA',
            'app_name': 'erpnext',
            'restrict_to_domain': None,
            'hidden': 0,
            'custom': 1
        }).insert()
    
    # Create ZATCA Settings doctype
    if not frappe.db.exists("DocType", "ZATCA Settings"):
        with open('zatca_settings.json', 'r') as f:
            settings_config = json.load(f)
        
        frappe.get_doc(settings_config).insert()
    
    # Create ZATCA Log doctype
    if not frappe.db.exists("DocType", "ZATCA Log"):
        with open('zatca_log.json', 'r') as f:
            log_config = json.load(f)
        
        frappe.get_doc(log_config).insert()
    
    # Add custom fields to Sales Invoice
    extend_sales_invoice()
    
    # Create default ZATCA Settings
    if not frappe.db.exists("ZATCA Settings", "Default"):
        frappe.get_doc({
            'doctype': 'ZATCA Settings',
            'name': 'Default',
            'api_key': '',
            'secret_key': '',
            'vat_number': '',
            'company_name': '',
            'base_url': 'https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal',
            'test_mode': 1
        }).insert()
    
    print("✅ ZATCA Phase 2 Module installed successfully!")
    print("\n📋 Next Steps:")
    print("1. Configure ZATCA Settings with your API credentials")
    print("2. Update your VAT number and company details")
    print("3. Test with a sample invoice")
    print("4. Enable automatic processing for new invoices")

def extend_sales_invoice():
    """Add ZATCA fields to Sales Invoice"""
    custom_fields = [
        {
            'fieldname': 'zatca_status',
            'label': 'ZATCA Status',
            'fieldtype': 'Data',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_clearance_status',
            'label': 'ZATCA Clearance Status',
            'fieldtype': 'Data',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_reporting_status',
            'label': 'ZATCA Reporting Status',
            'fieldtype': 'Data',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_qr_code',
            'label': 'ZATCA QR Code',
            'fieldtype': 'Code',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_signature',
            'label': 'ZATCA Signature',
            'fieldtype': 'Code',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_xml_content',
            'label': 'ZATCA XML Content',
            'fieldtype': 'Code',
            'read_only': 1
        }
    ]
    
    for field_config in custom_fields:
        if not frappe.db.exists("Custom Field", f"Sales Invoice-{field_config['fieldname']}"):
            frappe.get_doc({
                'doctype': 'Custom Field',
                'dt': 'Sales Invoice',
                'fieldname': field_config['fieldname'],
                'label': field_config['label'],
                'fieldtype': field_config['fieldtype'],
                'read_only': field_config['read_only']
            }).insert()

if __name__ == "__main__":
    install_zatca_module() 