#!/usr/bin/env python3
"""
SEIDiT ZATCA Phase 2 Module Installation Script
================================================

Official SEIDiT implementation of ZATCA (Zakat, Tax and Customs Authority) 
Phase 2 e-invoicing compliance for ERPNext.

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.

This script installs the complete SEIDiT ZATCA Phase 2 module including:
- Core ZATCA compliance functionality
- SEIDiT branded setup wizard
- Professional UI/UX design
- Complete documentation and support

For support and documentation, visit: https://seidit.com/zatca
"""

import frappe
import os
import json

class SEIDiTZATCAInstaller:
    """
    SEIDiT ZATCA Phase 2 Module Installer
    
    Professional installation and setup for SEIDiT's ZATCA implementation.
    """
    
    def __init__(self):
        self.provider = "SEIDiT"
        self.website = "https://seidit.com"
        self.support_email = "support@seidit.com"
        self.documentation_url = "https://seidit.com/zatca/docs"
        self.version = "2.0.0"
        
    def install_seidit_zatca_module(self):
        """Install SEIDiT ZATCA Phase 2 module with professional branding"""
        
        print("🚀 Installing SEIDiT ZATCA Phase 2 Module...")
        print(f"Provider: {self.provider}")
        print(f"Version: {self.version}")
        print(f"Website: {self.website}")
        print("=" * 60)
        
        # Create SEIDiT ZATCA module
        if not frappe.db.exists("Module Def", "SEIDiT ZATCA"):
            frappe.get_doc({
                'doctype': 'Module Def',
                'module_name': 'SEIDiT ZATCA',
                'app_name': 'erpnext',
                'restrict_to_domain': None,
                'hidden': 0,
                'custom': 1,
                'description': 'Official SEIDiT implementation of ZATCA Phase 2 e-invoicing compliance'
            }).insert()
            print("✅ Created SEIDiT ZATCA module")
        
        # Create all doctypes
        self.create_doctypes()
        
        # Create ERPNext page
        self.create_wizard_page()
        
        # Add custom fields to Sales Invoice
        self.extend_sales_invoice()
        
        # Create default settings
        self.create_default_settings()
        
        # Create wizard data
        self.create_wizard_data()
        
        # Create menu items
        self.create_menu_items()
        
        # Setup automatic processing
        self.setup_automatic_processing()
        
        # Create help documentation
        self.create_help_documentation()
        
        print("\n🎉 SEIDiT ZATCA Phase 2 Module installed successfully!")
        print("\n📋 Next Steps:")
        print("1. Go to ERPNext and look for 'SEIDiT ZATCA Setup Wizard' in the menu")
        print("2. Follow the step-by-step wizard to configure ZATCA")
        print("3. The wizard will guide you through:")
        print("   - VAT registration verification")
        print("   - Getting API credentials from ZATCA portal")
        print("   - Testing connection")
        print("   - Creating test invoices")
        print("   - Switching to live mode")
        print("\n🔗 Quick Access:")
        print("- Setup Wizard: /app/seidit-zatca-setup-wizard")
        print("- ZATCA Settings: /app/zatca-settings")
        print("- ZATCA Logs: /app/zatca-log")
        print("\n📞 SEIDiT Support:")
        print(f"- Website: {self.website}")
        print(f"- Support: {self.website}/support")
        print(f"- Email: {self.support_email}")
        print(f"- Documentation: {self.documentation_url}")

    def create_doctypes(self):
        """Create all required doctypes with SEIDiT branding"""
        
        # ZATCA Settings
        if not frappe.db.exists("DocType", "ZATCA Settings"):
            with open('zatca_settings.json', 'r') as f:
                settings_config = json.load(f)
            settings_config['description'] = 'SEIDiT ZATCA Settings - Configure your ZATCA API credentials and settings'
            frappe.get_doc(settings_config).insert()
            print("✅ Created ZATCA Settings doctype")
        
        # ZATCA Log
        if not frappe.db.exists("DocType", "ZATCA Log"):
            with open('zatca_log.json', 'r') as f:
                log_config = json.load(f)
            log_config['description'] = 'SEIDiT ZATCA Log - Track all ZATCA API interactions and processing history'
            frappe.get_doc(log_config).insert()
            print("✅ Created ZATCA Log doctype")
        
        # ZATCA Setup Wizard
        if not frappe.db.exists("DocType", "ZATCA Setup Wizard"):
            with open('zatca_setup_wizard.json', 'r') as f:
                wizard_config = json.load(f)
            wizard_config['description'] = 'SEIDiT ZATCA Setup Wizard - Guided setup for ZATCA Phase 2 compliance'
            frappe.get_doc(wizard_config).insert()
            print("✅ Created ZATCA Setup Wizard doctype")

    def create_wizard_page(self):
        """Create the SEIDiT wizard page in ERPNext"""
        
        if not frappe.db.exists("Page", "seidit-zatca-setup-wizard"):
            with open('zatca_wizard_page.json', 'r') as f:
                page_config = json.load(f)
            page_config['name'] = 'seidit-zatca-setup-wizard'
            page_config['title'] = 'SEIDiT ZATCA Setup Wizard'
            page_config['module'] = 'SEIDiT ZATCA'
            page_config['route'] = 'seidit-zatca-setup-wizard'
            frappe.get_doc(page_config).insert()
            print("✅ Created SEIDiT ZATCA Setup Wizard page")

    def extend_sales_invoice(self):
        """Add SEIDiT ZATCA fields to Sales Invoice"""
        
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
            },
            {
                'fieldname': 'zatca_provider',
                'label': 'ZATCA Provider',
                'fieldtype': 'Data',
                'read_only': 1,
                'default': 'SEIDiT'
            },
            {
                'fieldname': 'zatca_module_version',
                'label': 'ZATCA Module Version',
                'fieldtype': 'Data',
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
                    'read_only': field_config['read_only'],
                    'default': field_config.get('default', '')
                }).insert()
        
        print("✅ Added SEIDiT ZATCA fields to Sales Invoice")

    def create_default_settings(self):
        """Create default SEIDiT ZATCA Settings"""
        
        if not frappe.db.exists("ZATCA Settings", "Default"):
            frappe.get_doc({
                'doctype': 'ZATCA Settings',
                'name': 'Default',
                'api_key': '',
                'secret_key': '',
                'vat_number': '',
                'company_name': '',
                'base_url': 'https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal',
                'test_mode': 1,
                'provider': 'SEIDiT',
                'module_version': self.version
            }).insert()
            print("✅ Created default SEIDiT ZATCA Settings")

    def create_wizard_data(self):
        """Create initial SEIDiT wizard data"""
        
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
                'setup_complete': 0,
                'provider': 'SEIDiT',
                'module_version': self.version
            }).insert()
            print("✅ Created SEIDiT ZATCA Setup Wizard data")

    def create_menu_items(self):
        """Create menu items for easy access with SEIDiT branding"""
        
        # Add to main menu
        if not frappe.db.exists("Menu Item", "SEIDiT ZATCA Setup Wizard"):
            frappe.get_doc({
                'doctype': 'Menu Item',
                'name': 'SEIDiT ZATCA Setup Wizard',
                'label': 'SEIDiT ZATCA Setup Wizard',
                'icon': 'fa fa-cogs',
                'module': 'SEIDiT ZATCA',
                'page': 'seidit-zatca-setup-wizard',
                'parent': 'SEIDiT ZATCA',
                'order': 1
            }).insert()
        
        # Add ZATCA Settings menu
        if not frappe.db.exists("Menu Item", "SEIDiT ZATCA Settings"):
            frappe.get_doc({
                'doctype': 'Menu Item',
                'name': 'SEIDiT ZATCA Settings',
                'label': 'SEIDiT ZATCA Settings',
                'icon': 'fa fa-cog',
                'module': 'SEIDiT ZATCA',
                'doctype': 'ZATCA Settings',
                'parent': 'SEIDiT ZATCA',
                'order': 2
            }).insert()
        
        # Add ZATCA Logs menu
        if not frappe.db.exists("Menu Item", "SEIDiT ZATCA Logs"):
            frappe.get_doc({
                'doctype': 'Menu Item',
                'name': 'SEIDiT ZATCA Logs',
                'label': 'SEIDiT ZATCA Logs',
                'icon': 'fa fa-list',
                'module': 'SEIDiT ZATCA',
                'doctype': 'ZATCA Log',
                'parent': 'SEIDiT ZATCA',
                'order': 3
            }).insert()
        
        print("✅ Created SEIDiT menu items")

    def setup_automatic_processing(self):
        """Setup automatic invoice processing with SEIDiT branding"""
        
        # Create server script for automatic processing
        if not frappe.db.exists("Server Script", "SEIDiT ZATCA Auto Process"):
            frappe.get_doc({
                'doctype': 'Server Script',
                'name': 'SEIDiT ZATCA Auto Process',
                'script_type': 'DocType Event',
                'reference_doctype': 'Sales Invoice',
                'event': 'on_submit',
                'script': '''
# SEIDiT ZATCA Automatic Processing
from zatca_phase2_module import SEIDiTZATCAPhase2Module

def on_sales_invoice_submit(doc, method):
    """Automatically process invoice for ZATCA when submitted using SEIDiT implementation"""
    if doc.docstatus == 1:  # Submitted
        try:
            zatca = SEIDiTZATCAPhase2Module()
            result = zatca.process_invoice(doc.name)
            
            if result.get('status') == 'success':
                frappe.msgprint('✅ SEIDiT ZATCA processing successful!')
            else:
                frappe.msgprint(f'⚠️ SEIDiT ZATCA processing failed: {result.get("message")}')
                
        except Exception as e:
            frappe.log_error(f'SEIDiT ZATCA Processing Error: {str(e)}')
            frappe.msgprint(f'❌ SEIDiT ZATCA processing error: {str(e)}')
'''
            }).insert()
            print("✅ Created SEIDiT automatic processing script")

    def create_help_documentation(self):
        """Create SEIDiT help documentation"""
        
        if not frappe.db.exists("Web Page", "seidit-zatca-help"):
            frappe.get_doc({
                'doctype': 'Web Page',
                'title': 'SEIDiT ZATCA Phase 2 Help',
                'route': 'seidit-zatca-help',
                'published': 1,
                'content': f'''
# SEIDiT ZATCA Phase 2 Setup Guide

## About SEIDiT

**SEIDiT** is the official provider of ZATCA Phase 2 e-invoicing compliance solutions for ERPNext.

- **Website**: {self.website}
- **Support**: {self.website}/support
- **Email**: {self.support_email}
- **Documentation**: {self.documentation_url}

## Quick Start

1. **Access Setup Wizard**: Go to SEIDiT ZATCA Setup Wizard in the menu
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

## SEIDiT Features

- ✅ **Professional Support**: 24/7 SEIDiT support
- ✅ **Easy Setup**: Step-by-step wizard
- ✅ **Secure**: Encrypted credential storage
- ✅ **Compliant**: Full ZATCA Phase 2 compliance
- ✅ **Reliable**: Enterprise-grade implementation

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check internet connection
   - Verify API credentials
   - Contact SEIDiT support

2. **VAT Number Invalid**
   - Verify VAT number format
   - Check VAT registration status
   - Contact ZATCA support

3. **Invoice Processing Failed**
   - Check invoice data completeness
   - Verify tax calculations
   - Review SEIDiT logs

### Getting Help

- **SEIDiT Support**: {self.website}/support
- **Email Support**: {self.support_email}
- **Documentation**: {self.documentation_url}
- **ZATCA Portal**: https://gw-fatoorah.zatca.gov.sa

## Compliance Notes

- Ensure your VAT number is registered with ZATCA
- Test thoroughly before going live
- Monitor clearance status regularly
- Keep API credentials secure
- Maintain proper invoice numbering

## SEIDiT Warranty

SEIDiT provides professional support and warranty for all ZATCA implementations.
Contact us for enterprise support and custom solutions.

**SEIDiT - Your Trusted ZATCA Partner**
'''
            }).insert()
            print("✅ Created SEIDiT help documentation")

if __name__ == "__main__":
    installer = SEIDiTZATCAInstaller()
    installer.install_seidit_zatca_module() 