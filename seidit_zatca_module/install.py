"""
SEIDiT ZATCA Module Installation
================================

Installation script for SEIDiT ZATCA Phase 2 module.
Creates all required doctypes and configurations.

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.
"""

import frappe
import json

def install():
    """Install SEIDiT ZATCA Module"""
    
    print("🚀 Installing SEIDiT ZATCA Phase 2 Module...")
    
    # Create ZATCA Settings doctype
    create_zatca_settings_doctype()
    
    # Create ZATCA Log doctype
    create_zatca_log_doctype()
    
    # Create ZATCA Setup Wizard doctype
    create_zatca_setup_wizard_doctype()
    
    # Add custom fields to Sales Invoice
    add_sales_invoice_fields()
    
    # Create default settings
    create_default_settings()
    
    # Create menu items
    create_menu_items()
    
    print("✅ SEIDiT ZATCA Module installed successfully!")

def create_zatca_settings_doctype():
    """Create ZATCA Settings doctype"""
    if not frappe.db.exists("DocType", "ZATCA Settings"):
        frappe.get_doc({
            'doctype': 'DocType',
            'name': 'ZATCA Settings',
            'module': 'SEIDiT ZATCA',
            'custom': 1,
            'istable': 0,
            'issingle': 1,
            'fields': [
                {
                    'fieldname': 'company_name',
                    'label': 'Company Name',
                    'fieldtype': 'Data',
                    'reqd': 1
                },
                {
                    'fieldname': 'company_tax_number',
                    'label': 'VAT Number',
                    'fieldtype': 'Data',
                    'reqd': 1,
                    'description': '15-digit VAT registration number'
                },
                {
                    'fieldname': 'zatca_client_id',
                    'label': 'ZATCA API Key',
                    'fieldtype': 'Password',
                    'reqd': 1
                },
                {
                    'fieldname': 'zatca_client_secret',
                    'label': 'ZATCA Secret Key',
                    'fieldtype': 'Password',
                    'reqd': 1
                },
                {
                    'fieldname': 'zatca_certificate_path',
                    'label': 'Certificate Path',
                    'fieldtype': 'Data',
                    'description': 'Path to ZATCA public certificate file'
                },
                {
                    'fieldname': 'zatca_private_key_path',
                    'label': 'Private Key Path',
                    'fieldtype': 'Data',
                    'description': 'Path to ZATCA private key file'
                },
                {
                    'fieldname': 'test_mode',
                    'label': 'Test Mode',
                    'fieldtype': 'Check',
                    'default': 1,
                    'description': 'Enable test mode for safe testing'
                },
                {
                    'fieldname': 'current_step',
                    'label': 'Current Step',
                    'fieldtype': 'Int',
                    'default': 1,
                    'hidden': 1
                },
                {
                    'fieldname': 'setup_completed',
                    'label': 'Setup Completed',
                    'fieldtype': 'Check',
                    'default': 0,
                    'hidden': 1
                },
                {
                    'fieldname': 'seidit_license_key',
                    'label': 'SEIDiT License Key',
                    'fieldtype': 'Password',
                    'description': 'SEIDiT license key for unlimited usage'
                },
                {
                    'fieldname': 'seidit_license_active',
                    'label': 'License Active',
                    'fieldtype': 'Check',
                    'default': 0,
                    'description': 'SEIDiT license activation status'
                }
            ]
        }).insert()
        print("✅ Created ZATCA Settings doctype")

def create_zatca_log_doctype():
    """Create ZATCA Log doctype"""
    if not frappe.db.exists("DocType", "ZATCA Log"):
        frappe.get_doc({
            'doctype': 'DocType',
            'name': 'ZATCA Log',
            'module': 'SEIDiT ZATCA',
            'custom': 1,
            'istable': 0,
            'issingle': 0,
            'fields': [
                {
                    'fieldname': 'invoice',
                    'label': 'Invoice',
                    'fieldtype': 'Link',
                    'options': 'Sales Invoice',
                    'reqd': 1
                },
                {
                    'fieldname': 'status',
                    'label': 'Status',
                    'fieldtype': 'Select',
                    'options': 'success\nerror\nprocessing\nsubmitted\ncleared\nrejected',
                    'reqd': 1
                },
                {
                    'fieldname': 'response',
                    'label': 'ZATCA Response',
                    'fieldtype': 'Code',
                    'options': 'JSON'
                },
                {
                    'fieldname': 'status_code',
                    'label': 'Status Code',
                    'fieldtype': 'Int'
                },
                {
                    'fieldname': 'timestamp',
                    'label': 'Timestamp',
                    'fieldtype': 'Datetime',
                    'default': 'now'
                },
                {
                    'fieldname': 'provider',
                    'label': 'Provider',
                    'fieldtype': 'Data',
                    'default': 'SEIDiT',
                    'read_only': 1
                }
            ]
        }).insert()
        print("✅ Created ZATCA Log doctype")

def create_zatca_setup_wizard_doctype():
    """Create ZATCA Setup Wizard doctype"""
    if not frappe.db.exists("DocType", "ZATCA Setup Wizard"):
        frappe.get_doc({
            'doctype': 'DocType',
            'name': 'ZATCA Setup Wizard',
            'module': 'SEIDiT ZATCA',
            'custom': 1,
            'istable': 0,
            'issingle': 1,
            'fields': [
                {
                    'fieldname': 'current_step',
                    'label': 'Current Step',
                    'fieldtype': 'Int',
                    'default': 1
                },
                {
                    'fieldname': 'setup_completed',
                    'label': 'Setup Completed',
                    'fieldtype': 'Check',
                    'default': 0
                }
            ]
        }).insert()
        print("✅ Created ZATCA Setup Wizard doctype")

def add_sales_invoice_fields():
    """Add ZATCA fields to Sales Invoice"""
    custom_fields = [
        {
            'fieldname': 'zatca_status',
            'label': 'ZATCA Status',
            'fieldtype': 'Select',
            'options': 'pending\nprocessing\nsuccess\nerror\nsubmitted\ncleared\nrejected',
            'read_only': 1,
            'insert_after': 'status'
        },
        {
            'fieldname': 'zatca_clearance_status',
            'label': 'ZATCA Clearance Status',
            'fieldtype': 'Data',
            'read_only': 1,
            'insert_after': 'zatca_status'
        },
        {
            'fieldname': 'zatca_reporting_status',
            'label': 'ZATCA Reporting Status',
            'fieldtype': 'Data',
            'read_only': 1,
            'insert_after': 'zatca_clearance_status'
        },
        {
            'fieldname': 'zatca_qr_code',
            'label': 'ZATCA QR Code',
            'fieldtype': 'Code',
            'read_only': 1,
            'insert_after': 'zatca_reporting_status'
        },
        {
            'fieldname': 'zatca_signature',
            'label': 'ZATCA Signature',
            'fieldtype': 'Code',
            'read_only': 1,
            'insert_after': 'zatca_qr_code'
        },
        {
            'fieldname': 'zatca_xml_content',
            'label': 'ZATCA XML Content',
            'fieldtype': 'Code',
            'read_only': 1,
            'insert_after': 'zatca_signature'
        },
        {
            'fieldname': 'zatca_provider',
            'label': 'ZATCA Provider',
            'fieldtype': 'Data',
            'read_only': 1,
            'default': 'SEIDiT',
            'insert_after': 'zatca_xml_content'
        },
        {
            'fieldname': 'zatca_module_version',
            'label': 'ZATCA Module Version',
            'fieldtype': 'Data',
            'read_only': 1,
            'insert_after': 'zatca_provider'
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", f"Sales Invoice-{field['fieldname']}"):
            frappe.get_doc({
                'doctype': 'Custom Field',
                'dt': 'Sales Invoice',
                **field
            }).insert()
    
    print("✅ Added ZATCA fields to Sales Invoice")

def create_default_settings():
    """Create default ZATCA settings"""
    if not frappe.db.exists("ZATCA Settings", "Default"):
        frappe.get_doc({
            'doctype': 'ZATCA Settings',
            'company_name': '',
            'company_tax_number': '',
            'zatca_client_id': '',
            'zatca_client_secret': '',
            'zatca_certificate_path': '',
            'zatca_private_key_path': '',
            'test_mode': 1,
            'current_step': 1,
            'setup_completed': 0,
            'seidit_license_key': '',
            'seidit_license_active': 0
        }).insert()
        print("✅ Created default ZATCA settings")

def create_menu_items():
    """Create menu items for ZATCA module"""
    
    # Create ZATCA menu
    if not frappe.db.exists("Page", "zatca-setup-wizard"):
        frappe.get_doc({
            'doctype': 'Page',
            'name': 'zatca-setup-wizard',
            'title': 'ZATCA Setup Wizard',
            'module': 'SEIDiT ZATCA',
            'template': 'zatca-setup-wizard.html',
            'published': 1
        }).insert()
        print("✅ Created ZATCA Setup Wizard page")
    
    # Create menu item in Desk
    if not frappe.db.exists("Desktop Icon", "ZATCA Setup Wizard"):
        frappe.get_doc({
            'doctype': 'Desktop Icon',
            'module_name': 'SEIDiT ZATCA',
            'label': 'ZATCA Setup Wizard',
            'icon': 'octicon octicon-gear',
            'type': 'page',
            'link': 'zatca-setup-wizard',
            'color': '#007bff',
            'description': 'Complete ZATCA Phase 2 setup wizard',
            'category': 'Integrations'
        }).insert()
        print("✅ Created ZATCA Setup Wizard menu item")
    
    # Create ZATCA Settings menu item
    if not frappe.db.exists("Desktop Icon", "ZATCA Settings"):
        frappe.get_doc({
            'doctype': 'Desktop Icon',
            'module_name': 'SEIDiT ZATCA',
            'label': 'ZATCA Settings',
            'icon': 'octicon octicon-settings',
            'type': 'doctype',
            'link': 'ZATCA Settings',
            'color': '#28a745',
            'description': 'Configure ZATCA settings and credentials',
            'category': 'Integrations'
        }).insert()
        print("✅ Created ZATCA Settings menu item")
    
    # Create ZATCA Logs menu item
    if not frappe.db.exists("Desktop Icon", "ZATCA Logs"):
        frappe.get_doc({
            'doctype': 'Desktop Icon',
            'module_name': 'SEIDiT ZATCA',
            'label': 'ZATCA Logs',
            'icon': 'octicon octicon-list-ordered',
            'type': 'doctype',
            'link': 'ZATCA Log',
            'color': '#ffc107',
            'description': 'View ZATCA processing logs and status',
            'category': 'Integrations'
        }).insert()
        print("✅ Created ZATCA Logs menu item")
    
    print("✅ Created all menu items")

def uninstall():
    """Uninstall SEIDiT ZATCA Module"""
    print("🗑️ Uninstalling SEIDiT ZATCA Module...")
    
    # Remove custom fields
    custom_fields = [
        'zatca_status',
        'zatca_clearance_status', 
        'zatca_reporting_status',
        'zatca_qr_code',
        'zatca_signature',
        'zatca_xml_content',
        'zatca_provider',
        'zatca_module_version'
    ]
    
    for field in custom_fields:
        if frappe.db.exists("Custom Field", f"Sales Invoice-{field}"):
            frappe.delete_doc("Custom Field", f"Sales Invoice-{field}")
    
    # Remove doctypes
    doctypes = ["ZATCA Settings", "ZATCA Log", "ZATCA Setup Wizard"]
    for doctype in doctypes:
        if frappe.db.exists("DocType", doctype):
            frappe.delete_doc("DocType", doctype)
    
    # Remove pages
    if frappe.db.exists("Page", "zatca-setup-wizard"):
        frappe.delete_doc("Page", "zatca-setup-wizard")
    
    # Remove desktop icons
    if frappe.db.exists("Desktop Icon", "ZATCA Setup Wizard"):
        frappe.delete_doc("Desktop Icon", "ZATCA Setup Wizard")
    
    print("✅ SEIDiT ZATCA Module uninstalled successfully!") 