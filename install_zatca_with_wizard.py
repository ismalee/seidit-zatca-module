#!/usr/bin/env python3
"""
Enhanced ZATCA Phase 2 Module Installation Script with Setup Wizard
"""

import frappe
import os
import json

def install_zatca_with_wizard():
    """Install ZATCA Phase 2 module with setup wizard"""
    
    print("🚀 Installing ZATCA Phase 2 Module with Setup Wizard...")
    
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
        print("✅ Created ZATCA module")
    
    # Create all doctypes
    create_doctypes()
    
    # Create ERPNext page
    create_wizard_page()
    
    # Add custom fields to Sales Invoice
    extend_sales_invoice()
    
    # Create default settings
    create_default_settings()
    
    # Create wizard data
    create_wizard_data()
    
    print("\n🎉 ZATCA Phase 2 Module with Setup Wizard installed successfully!")
    print("\n📋 Next Steps:")
    print("1. Go to ERPNext and look for 'ZATCA Setup Wizard' in the menu")
    print("2. Follow the step-by-step wizard to configure ZATCA")
    print("3. The wizard will guide you through:")
    print("   - VAT registration verification")
    print("   - Getting API credentials from ZATCA portal")
    print("   - Testing connection")
    print("   - Creating test invoices")
    print("   - Switching to live mode")
    print("\n🔗 Quick Access:")
    print("- Setup Wizard: /app/zatca-setup-wizard")
    print("- ZATCA Settings: /app/zatca-settings")
    print("- ZATCA Logs: /app/zatca-log")

def create_doctypes():
    """Create all required doctypes"""
    
    # ZATCA Settings
    if not frappe.db.exists("DocType", "ZATCA Settings"):
        with open('zatca_settings.json', 'r') as f:
            settings_config = json.load(f)
        frappe.get_doc(settings_config).insert()
        print("✅ Created ZATCA Settings doctype")
    
    # ZATCA Log
    if not frappe.db.exists("DocType", "ZATCA Log"):
        with open('zatca_log.json', 'r') as f:
            log_config = json.load(f)
        frappe.get_doc(log_config).insert()
        print("✅ Created ZATCA Log doctype")
    
    # ZATCA Setup Wizard
    if not frappe.db.exists("DocType", "ZATCA Setup Wizard"):
        with open('zatca_setup_wizard.json', 'r') as f:
            wizard_config = json.load(f)
        frappe.get_doc(wizard_config).insert()
        print("✅ Created ZATCA Setup Wizard doctype")

def create_wizard_page():
    """Create the wizard page in ERPNext"""
    
    if not frappe.db.exists("Page", "zatca-setup-wizard"):
        with open('zatca_wizard_page.json', 'r') as f:
            page_config = json.load(f)
        frappe.get_doc(page_config).insert()
        print("✅ Created ZATCA Setup Wizard page")
    
    # Add page to menu
    if not frappe.db.exists("Page", "zatca-setup-wizard"):
        frappe.get_doc({
            'doctype': 'Page',
            'name': 'zatca-setup-wizard',
            'title': 'ZATCA Setup Wizard',
            'icon': 'fa fa-cogs',
            'module': 'ZATCA',
            'is_standard': 0,
            'published': 1,
            'route': 'zatca-setup-wizard'
        }).insert()

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
    
    print("✅ Added ZATCA fields to Sales Invoice")

def create_default_settings():
    """Create default ZATCA Settings"""
    
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
        print("✅ Created default ZATCA Settings")

def create_wizard_data():
    """Create initial wizard data"""
    
    if not frappe.db.exists("ZATCA Setup Wizard", "Default"):
        frappe.get_doc({
            'doctype': 'ZATCA Setup Wizard',
            'name': 'Default',
            'current_step': 'welcome',
            'vat_number': '',
            'company_name': '',
            'zatca_username': '',
            'zatca_password': '',
            'api_key': '',
            'secret_key': '',
            'test_mode': 1,
            'setup_complete': 0
        }).insert()
        print("✅ Created ZATCA Setup Wizard data")

def create_menu_items():
    """Create menu items for easy access"""
    
    # Add to main menu
    if not frappe.db.exists("Menu Item", "ZATCA Setup Wizard"):
        frappe.get_doc({
            'doctype': 'Menu Item',
            'name': 'ZATCA Setup Wizard',
            'label': 'ZATCA Setup Wizard',
            'icon': 'fa fa-cogs',
            'module': 'ZATCA',
            'page': 'zatca-setup-wizard',
            'parent': 'ZATCA',
            'order': 1
        }).insert()
    
    # Add ZATCA Settings menu
    if not frappe.db.exists("Menu Item", "ZATCA Settings"):
        frappe.get_doc({
            'doctype': 'Menu Item',
            'name': 'ZATCA Settings',
            'label': 'ZATCA Settings',
            'icon': 'fa fa-cog',
            'module': 'ZATCA',
            'doctype': 'ZATCA Settings',
            'parent': 'ZATCA',
            'order': 2
        }).insert()
    
    # Add ZATCA Logs menu
    if not frappe.db.exists("Menu Item", "ZATCA Logs"):
        frappe.get_doc({
            'doctype': 'Menu Item',
            'name': 'ZATCA Logs',
            'label': 'ZATCA Logs',
            'icon': 'fa fa-list',
            'module': 'ZATCA',
            'doctype': 'ZATCA Log',
            'parent': 'ZATCA',
            'order': 3
        }).insert()
    
    print("✅ Created menu items")

def setup_automatic_processing():
    """Setup automatic invoice processing"""
    
    # Create server script for automatic processing
    if not frappe.db.exists("Server Script", "ZATCA Auto Process"):
        frappe.get_doc({
            'doctype': 'Server Script',
            'name': 'ZATCA Auto Process',
            'script_type': 'DocType Event',
            'reference_doctype': 'Sales Invoice',
            'event': 'on_submit',
            'script': '''
# ZATCA Automatic Processing
from zatca_phase2_module import ZATCAPhase2Module

def on_sales_invoice_submit(doc, method):
    """Automatically process invoice for ZATCA when submitted"""
    if doc.docstatus == 1:  # Submitted
        try:
            zatca = ZATCAPhase2Module()
            result = zatca.process_invoice(doc.name)
            
            if result.get('status') == 'success':
                frappe.msgprint('✅ Invoice processed for ZATCA successfully!')
            else:
                frappe.msgprint(f'⚠️ ZATCA processing failed: {result.get("message")}')
                
        except Exception as e:
            frappe.log_error(f'ZATCA Processing Error: {str(e)}')
            frappe.msgprint(f'❌ ZATCA processing error: {str(e)}')
'''
        }).insert()
        print("✅ Created automatic processing script")

def create_help_documentation():
    """Create help documentation"""
    
    if not frappe.db.exists("Web Page", "zatca-help"):
        frappe.get_doc({
            'doctype': 'Web Page',
            'title': 'ZATCA Phase 2 Help',
            'route': 'zatca-help',
            'published': 1,
            'content': '''
# ZATCA Phase 2 Setup Guide

## Quick Start

1. **Access Setup Wizard**: Go to ZATCA Setup Wizard in the menu
2. **Follow Steps**: Complete each step in the wizard
3. **Test**: Create test invoices to verify setup
4. **Go Live**: Switch to live mode when ready

## Step-by-Step Guide

### Step 1: VAT Registration
- Enter your 15-digit VAT number
- Verify company name matches VAT certificate

### Step 2: ZATCA Portal Access
- Click "Test Portal" or "Live Portal" buttons
- Login with your VAT credentials
- Navigate to Developer Portal section

### Step 3: API Credentials
- Generate API key and secret key in ZATCA portal
- Copy credentials to the wizard
- Enable test mode for initial testing

### Step 4: Test Connection
- Test API connection with ZATCA
- Verify credentials are working
- Check VAT number validation

### Step 5: Invoice Testing
- Create test invoice
- Verify ZATCA processing
- Check clearance status

### Step 6: Live Activation
- Disable test mode
- Update live API credentials
- Test with real invoice

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check internet connection
   - Verify API credentials
   - Ensure correct portal URL

2. **VAT Number Invalid**
   - Verify VAT number format
   - Check VAT registration status
   - Contact ZATCA support

3. **Invoice Processing Failed**
   - Check invoice data completeness
   - Verify tax calculations
   - Review error logs

### Getting Help

- Check ZATCA Logs for detailed error messages
- Review ZATCA Settings configuration
- Contact ZATCA support for portal issues
- Check ERPNext logs for system errors

## Compliance Notes

- Ensure VAT number is registered with ZATCA
- Test thoroughly before going live
- Monitor clearance status regularly
- Keep API credentials secure
- Maintain proper invoice numbering
'''
        }).insert()
        print("✅ Created help documentation")

if __name__ == "__main__":
    install_zatca_with_wizard()
    create_menu_items()
    setup_automatic_processing()
    create_help_documentation() 