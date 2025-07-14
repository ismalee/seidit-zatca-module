"""
SEIDiT ZATCA Setup Wizard
==========================

Professional setup wizard for ZATCA Phase 2 configuration.
Guides users through complete ZATCA setup process.

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.
"""

import frappe
import json
import hashlib
import requests
from datetime import datetime
import uuid

class ZATCASetupWizard:
    """ZATCA Setup Wizard with step-by-step guidance"""
    
    def __init__(self):
        self.provider = "SEIDiT"
        self.version = "2.0.0"
        self.website = "https://seidit.com"
        self.support_email = "support@seidit.com"
        self.support_whatsapp = "+966567414356"
        self.documentation_url = "https://seidit.com/zatca/docs"
        
    def get_wizard_data(self):
        """Get wizard data for setup"""
        try:
            # Get current settings
            settings = self._get_current_settings()
            
            # Get installation info
            installation_info = self._get_installation_info()
            
            # Get license status
            license_status = self._get_license_status()
            
            wizard_data = {
                'provider': self.provider,
                'version': self.version,
                'website': self.website,
                'support_email': self.support_email,
                'support_whatsapp': self.support_whatsapp,
                'documentation_url': self.documentation_url,
                'installation_info': installation_info,
                'license_status': license_status,
                'current_settings': settings,
                'steps': self._get_wizard_steps(),
                'current_step': settings.get('current_step', 1) if settings else 1
            }
            
            return {
                'status': 'success',
                'wizard_data': wizard_data
            }
            
        except Exception as e:
            frappe.log_error(f"ZATCA Wizard Data Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to get wizard data: {str(e)}'
            }
    
    def _get_current_settings(self):
        """Get current ZATCA settings"""
        try:
            if frappe.db.exists("ZATCA Settings", "Default"):
                settings = frappe.get_doc("ZATCA Settings", "Default")
                return {
                    'company_tax_number': settings.company_tax_number,
                    'company_name': settings.company_name,
                    'zatca_api_url': settings.zatca_api_url,
                    'zatca_client_id': settings.zatca_client_id,
                    'zatca_client_secret': settings.zatca_client_secret,
                    'zatca_certificate_path': settings.zatca_certificate_path,
                    'zatca_private_key_path': settings.zatca_private_key_path,
                    'zatca_mode': settings.zatca_mode,
                    'test_mode': settings.test_mode,
                    'current_step': settings.current_step,
                    'setup_completed': settings.setup_completed
                }
            else:
                return {}
                
        except Exception as e:
            frappe.log_error(f"ZATCA Settings Error: {str(e)}")
            return {}
    
    def _get_installation_info(self):
        """Get installation information"""
        try:
            # Generate unique installation ID
            system_info = {
                'platform': frappe.get_system_info().get('platform'),
                'site': frappe.local.site,
                'timestamp': datetime.now().isoformat()
            }
            
            installation_id = hashlib.sha256(
                json.dumps(system_info, sort_keys=True).encode()
            ).hexdigest()[:16].upper()
            
            return {
                'installation_id': f"SEIDiT_{installation_id}",
                'system_info': system_info,
                'provider': self.provider
            }
            
        except Exception as e:
            frappe.log_error(f"Installation Info Error: {str(e)}")
            return {
                'installation_id': f"SEIDiT_{uuid.uuid4().hex[:16].upper()}",
                'provider': self.provider
            }
    
    def _get_license_status(self):
        """Get license status"""
        try:
            # Check if license is active
            if frappe.db.exists("ZATCA Settings", "Default"):
                settings = frappe.get_doc("ZATCA Settings", "Default")
                if settings.seidit_license_active:
                    return {
                        'status': 'licensed',
                        'message': 'License is active',
                        'license_type': 'paid',
                        'usage_limit': 'unlimited'
                    }
            
            # Check free usage
            usage_count = self._get_usage_count()
            free_limit = 10
            
            if usage_count < free_limit:
                return {
                    'status': 'free_trial',
                    'message': f'Free trial: {usage_count}/{free_limit} invoices used',
                    'usage_count': usage_count,
                    'usage_limit': free_limit
                }
            else:
                return {
                    'status': 'license_required',
                    'message': f'Free trial limit reached ({free_limit} invoices). License required.',
                    'usage_count': usage_count,
                    'usage_limit': free_limit
                }
                
        except Exception as e:
            frappe.log_error(f"License Status Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'License status check failed: {str(e)}'
            }
    
    def _get_usage_count(self):
        """Get current usage count"""
        try:
            usage_count = frappe.db.count("ZATCA Log", filters={
                'status': ['in', ['success', 'submitted']]
            })
            return usage_count
            
        except Exception as e:
            frappe.log_error(f"Usage Count Error: {str(e)}")
            return 0
    
    def _get_wizard_steps(self):
        """Get wizard steps"""
        return [
            {
                'step': 1,
                'title': 'Welcome to ZATCA Setup',
                'description': 'Complete ZATCA Phase 2 compliance setup',
                'icon': '🎯',
                'status': 'pending',
                'fields': ['welcome_message']
            },
            {
                'step': 2,
                'title': 'Company Information',
                'description': 'Enter your company details and VAT registration',
                'icon': '🏢',
                'status': 'pending',
                'fields': ['company_name', 'company_tax_number']
            },
            {
                'step': 3,
                'title': 'ZATCA Portal Access',
                'description': 'Get API credentials from ZATCA portal',
                'icon': '🔑',
                'status': 'pending',
                'fields': ['zatca_portal_instructions']
            },
            {
                'step': 4,
                'title': 'API Configuration',
                'description': 'Configure ZATCA API credentials',
                'icon': '⚙️',
                'status': 'pending',
                'fields': ['zatca_client_id', 'zatca_client_secret', 'test_mode']
            },
            {
                'step': 5,
                'title': 'Certificate Setup',
                'description': 'Upload ZATCA certificates',
                'icon': '📜',
                'status': 'pending',
                'fields': ['zatca_certificate_path', 'zatca_private_key_path']
            },
            {
                'step': 6,
                'title': 'Test Connection',
                'description': 'Test ZATCA API connection',
                'icon': '🔗',
                'status': 'pending',
                'fields': ['test_connection']
            },
            {
                'step': 7,
                'title': 'Test Invoice',
                'description': 'Generate test invoice',
                'icon': '🧪',
                'status': 'pending',
                'fields': ['test_invoice']
            },
            {
                'step': 8,
                'title': 'License Information',
                'description': 'Review license status and limits',
                'icon': '🔐',
                'status': 'pending',
                'fields': ['license_info']
            },
            {
                'step': 9,
                'title': 'Live Mode',
                'description': 'Activate live mode for production',
                'icon': '🚀',
                'status': 'pending',
                'fields': ['live_mode_activation']
            }
        ]
    
    def update_settings(self, settings_data):
        """Update ZATCA settings"""
        try:
            if not frappe.db.exists("ZATCA Settings", "Default"):
                # Create default settings
                settings = frappe.get_doc({
                    'doctype': 'ZATCA Settings',
                    'company_name': settings_data.get('company_name', ''),
                    'company_tax_number': settings_data.get('company_tax_number', ''),
                    'zatca_api_url': settings_data.get('zatca_api_url', ''),
                    'zatca_client_id': settings_data.get('zatca_client_id', ''),
                    'zatca_client_secret': settings_data.get('zatca_client_secret', ''),
                    'zatca_certificate_path': settings_data.get('zatca_certificate_path', ''),
                    'zatca_private_key_path': settings_data.get('zatca_private_key_path', ''),
                    'zatca_mode': settings_data.get('zatca_mode', 'test'),
                    'test_mode': settings_data.get('test_mode', True),
                    'current_step': settings_data.get('current_step', 1),
                    'setup_completed': settings_data.get('setup_completed', False),
                    'provider': self.provider,
                    'version': self.version
                })
                settings.insert()
            else:
                # Update existing settings
                settings = frappe.get_doc("ZATCA Settings", "Default")
                settings.company_name = settings_data.get('company_name', settings.company_name)
                settings.company_tax_number = settings_data.get('company_tax_number', settings.company_tax_number)
                settings.zatca_api_url = settings_data.get('zatca_api_url', settings.zatca_api_url)
                settings.zatca_client_id = settings_data.get('zatca_client_id', settings.zatca_client_id)
                settings.zatca_client_secret = settings_data.get('zatca_client_secret', settings.zatca_client_secret)
                settings.zatca_certificate_path = settings_data.get('zatca_certificate_path', settings.zatca_certificate_path)
                settings.zatca_private_key_path = settings_data.get('zatca_private_key_path', settings.zatca_private_key_path)
                settings.zatca_mode = settings_data.get('zatca_mode', settings.zatca_mode)
                settings.test_mode = settings_data.get('test_mode', settings.test_mode)
                settings.current_step = settings_data.get('current_step', settings.current_step)
                settings.setup_completed = settings_data.get('setup_completed', settings.setup_completed)
                settings.save()
            
            return {
                'status': 'success',
                'message': 'Settings updated successfully'
            }
            
        except Exception as e:
            frappe.log_error(f"ZATCA Settings Update Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to update settings: {str(e)}'
            }
    
    def test_zatca_connection(self):
        """Test ZATCA API connection"""
        try:
            if not frappe.db.exists("ZATCA Settings", "Default"):
                return {
                    'status': 'error',
                    'message': 'ZATCA settings not configured'
                }
            
            settings = frappe.get_doc("ZATCA Settings", "Default")
            
            # Test API connection
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'OTP': settings.zatca_client_id,
                'Authorization': f'Bearer {settings.zatca_client_secret}'
            }
            
            # Test endpoint
            test_url = "https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal/compliance"
            
            response = requests.get(test_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'message': 'ZATCA API connection successful',
                    'response': response.json()
                }
            else:
                return {
                    'status': 'error',
                    'message': f'ZATCA API connection failed: {response.status_code}',
                    'response': response.text
                }
                
        except Exception as e:
            frappe.log_error(f"ZATCA Connection Test Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}'
            }
    
    def generate_test_invoice(self):
        """Generate test invoice for ZATCA"""
        try:
            # Create test customer
            if not frappe.db.exists("Customer", "Test Customer"):
                customer = frappe.get_doc({
                    'doctype': 'Customer',
                    'customer_name': 'Test Customer',
                    'customer_type': 'Company',
                    'customer_group': 'Commercial'
                })
                customer.insert()
            
            # Create test item
            if not frappe.db.exists("Item", "Test Item"):
                item = frappe.get_doc({
                    'doctype': 'Item',
                    'item_code': 'TEST-001',
                    'item_name': 'Test Item',
                    'item_group': 'Products',
                    'stock_uom': 'Nos',
                    'is_stock_item': 0
                })
                item.insert()
            
            # Create test invoice
            invoice = frappe.get_doc({
                'doctype': 'Sales Invoice',
                'customer': 'Test Customer',
                'posting_date': datetime.now().date(),
                'due_date': datetime.now().date(),
                'items': [
                    {
                        'item_code': 'TEST-001',
                        'qty': 1,
                        'rate': 100.00,
                        'amount': 100.00
                    }
                ]
            })
            invoice.insert()
            invoice.submit()
            
            # Process for ZATCA
            from zatca_core import ZATCAInvoiceProcessor
            processor = ZATCAInvoiceProcessor()
            result = processor.process_invoice(invoice.name)
            
            return {
                'status': 'success',
                'message': 'Test invoice generated and processed',
                'invoice_name': invoice.name,
                'zatca_result': result
            }
            
        except Exception as e:
            frappe.log_error(f"Test Invoice Generation Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Test invoice generation failed: {str(e)}'
            }
    
    def activate_live_mode(self):
        """Activate live mode"""
        try:
            if not frappe.db.exists("ZATCA Settings", "Default"):
                return {
                    'status': 'error',
                    'message': 'ZATCA settings not configured'
                }
            
            settings = frappe.get_doc("ZATCA Settings", "Default")
            settings.test_mode = False
            settings.setup_completed = True
            settings.current_step = 9
            settings.save()
            
            return {
                'status': 'success',
                'message': 'Live mode activated successfully'
            }
            
        except Exception as e:
            frappe.log_error(f"Live Mode Activation Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Live mode activation failed: {str(e)}'
            }

# API Endpoints
@frappe.whitelist()
def get_zatca_wizard_data():
    """Get ZATCA wizard data"""
    wizard = ZATCASetupWizard()
    return wizard.get_wizard_data()

@frappe.whitelist()
def update_zatca_settings(settings_data):
    """Update ZATCA settings"""
    wizard = ZATCASetupWizard()
    return wizard.update_settings(json.loads(settings_data))

@frappe.whitelist()
def test_zatca_connection():
    """Test ZATCA connection"""
    wizard = ZATCASetupWizard()
    return wizard.test_zatca_connection()

@frappe.whitelist()
def generate_test_invoice():
    """Generate test invoice"""
    wizard = ZATCASetupWizard()
    return wizard.generate_test_invoice()

@frappe.whitelist()
def activate_live_mode():
    """Activate live mode"""
    wizard = ZATCASetupWizard()
    return wizard.activate_live_mode() 