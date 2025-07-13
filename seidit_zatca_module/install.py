import frappe

def install():
    """Install SEIDiT ZATCA Module"""
    
    # Create ZATCA Setup Wizard doctype
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
                    'fieldname': 'step',
                    'label': 'Current Step',
                    'fieldtype': 'Select',
                    'options': 'Welcome\nVAT Registration\nZATCA Portal Access\nAPI Credentials\nTest Connection\nLive Activation\nInvoice Testing\nLicense Warning\nCompletion',
                    'default': 'Welcome'
                },
                {
                    'fieldname': 'vat_number',
                    'label': 'VAT Number',
                    'fieldtype': 'Data'
                },
                {
                    'fieldname': 'company_name',
                    'label': 'Company Name',
                    'fieldtype': 'Data'
                },
                {
                    'fieldname': 'api_key',
                    'label': 'API Key',
                    'fieldtype': 'Password'
                },
                {
                    'fieldname': 'secret_key',
                    'label': 'Secret Key',
                    'fieldtype': 'Password'
                },
                {
                    'fieldname': 'test_mode',
                    'label': 'Test Mode',
                    'fieldtype': 'Check',
                    'default': 1
                },
                {
                    'fieldname': 'installation_id',
                    'label': 'Installation ID',
                    'fieldtype': 'Data',
                    'read_only': 1
                }
            ]
        }).insert()
    
    # Create ZATCA Settings doctype
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
                    'fieldname': 'vat_number',
                    'label': 'VAT Number',
                    'fieldtype': 'Data',
                    'reqd': 1
                },
                {
                    'fieldname': 'company_name',
                    'label': 'Company Name',
                    'fieldtype': 'Data',
                    'reqd': 1
                },
                {
                    'fieldname': 'api_key',
                    'label': 'API Key',
                    'fieldtype': 'Password',
                    'reqd': 1
                },
                {
                    'fieldname': 'secret_key',
                    'label': 'Secret Key',
                    'fieldtype': 'Password',
                    'reqd': 1
                },
                {
                    'fieldname': 'test_mode',
                    'label': 'Test Mode',
                    'fieldtype': 'Check',
                    'default': 1
                },
                {
                    'fieldname': 'base_url',
                    'label': 'Base URL',
                    'fieldtype': 'Data',
                    'default': 'https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal'
                }
            ]
        }).insert()
    
    # Create default ZATCA Settings
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
    
    # Create default ZATCA Setup Wizard
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
    
    # Create menu items
    create_menu_items()
    
    print("✅ SEIDiT ZATCA Module installed successfully!")

def create_menu_items():
    """Create menu items for the ZATCA module"""
    
    # Create ZATCA Setup Wizard menu item
    if not frappe.db.exists("Page", "zatca-setup-wizard"):
        frappe.get_doc({
            'doctype': 'Page',
            'name': 'zatca-setup-wizard',
            'title': 'ZATCA Setup Wizard',
            'module': 'SEIDiT ZATCA',
            'icon': 'octicon octicon-gear',
            'route': '/app/zatca-setup-wizard'
        }).insert()
    
    # Create ZATCA Settings menu item
    if not frappe.db.exists("Page", "zatca-settings"):
        frappe.get_doc({
            'doctype': 'Page',
            'name': 'zatca-settings',
            'title': 'ZATCA Settings',
            'module': 'SEIDiT ZATCA',
            'icon': 'octicon octicon-settings',
            'route': '/app/zatca-settings'
        }).insert() 