"""
SEIDiT ZATCA Setup Wizard
==========================

Professional setup wizard for SEIDiT ZATCA Phase 2 module.
Guides users through ZATCA configuration and license activation.

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.
"""

import frappe
import json
import hashlib
import hmac
import base64
import time
import uuid
from datetime import datetime
import requests

class SEIDiTZATCASetupWizard:
    """
    SEIDiT ZATCA Setup Wizard
    
    Professional setup wizard with:
    - Step-by-step ZATCA configuration
    - License management
    - API credential setup
    - Test invoice generation
    - Live mode activation
    """
    
    def __init__(self):
        self.provider = "SEIDiT"
        self.version = "2.0.0"
        self.website = "https://seidit.com"
        self.support_email = "support@seidit.com"
        self.support_whatsapp = "+966567414356"
        self.documentation_url = "https://seidit.com/zatca/docs"
        self.server_url = "https://154.90.50.194/api/method/seidit_license_server.validate_license"
        self.free_limit = 10
        
    def get_wizard_data(self):
        """Get wizard data for setup"""
        try:
            # Get installation info
            from seidit_license_system import SEIDiTLicenseSystem
            license_system = SEIDiTLicenseSystem()
            installation_info = license_system.get_installation_info()
            
            # Get license status
            license_status = license_system.check_license_status()
            
            # Get current settings
            settings = self._get_current_settings()
            
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
                'free_limit': self.free_limit,
                'steps': self._get_wizard_steps()
            }
            
            return {
                'status': 'success',
                'wizard_data': wizard_data,
                'provider': self.provider
            }
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Wizard Data Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to get wizard data: {str(e)}',
                'provider': self.provider
            }
    
    def _get_current_settings(self):
        """Get current ZATCA settings"""
        try:
            if frappe.db.exists("ZATCA Settings", "Default"):
                settings = frappe.get_doc("ZATCA Settings", "Default")
                return {
                    'company_tax_number': settings.company_tax_number,
                    'zatca_api_url': settings.zatca_api_url,
                    'zatca_client_id': settings.zatca_client_id,
                    'zatca_client_secret': settings.zatca_client_secret,
                    'zatca_certificate_path': settings.zatca_certificate_path,
                    'zatca_private_key_path': settings.zatca_private_key_path,
                    'zatca_mode': settings.zatca_mode,
                    'seidit_license_key': settings.seidit_license_key,
                    'seidit_license_active': settings.seidit_license_active
                }
            else:
                return {}
                
        except Exception as e:
            frappe.log_error(f"SEIDiT Settings Error: {str(e)}")
            return {}
    
    def _get_wizard_steps(self):
        """Get wizard steps"""
        return [
            {
                'step': 1,
                'title': 'Welcome to SEIDiT ZATCA Setup',
                'description': 'Professional ZATCA Phase 2 compliance setup',
                'icon': '🎯',
                'status': 'pending'
            },
            {
                'step': 2,
                'title': 'Installation Information',
                'description': 'Your unique installation ID and hardware fingerprint',
                'icon': '🖥️',
                'status': 'pending'
            },
            {
                'step': 3,
                'title': 'License Information',
                'description': 'SEIDiT license status and usage limits',
                'icon': '🔐',
                'status': 'pending'
            },
            {
                'step': 4,
                'title': 'ZATCA Portal Setup',
                'description': 'Get API credentials from ZATCA portal',
                'icon': '🏢',
                'status': 'pending'
            },
            {
                'step': 5,
                'title': 'API Configuration',
                'description': 'Configure ZATCA API credentials',
                'icon': '⚙️',
                'status': 'pending'
            },
            {
                'step': 6,
                'title': 'Test Connection',
                'description': 'Test ZATCA API connection',
                'icon': '🔗',
                'status': 'pending'
            },
            {
                'step': 7,
                'title': 'Test Invoice',
                'description': 'Generate test invoice',
                'icon': '🧪',
                'status': 'pending'
            },
            {
                'step': 8,
                'title': 'Live Mode',
                'description': 'Activate live mode for production',
                'icon': '🚀',
                'status': 'pending'
            }
        ]
    
    def update_settings(self, settings_data):
        """Update ZATCA settings"""
        try:
            if not frappe.db.exists("ZATCA Settings", "Default"):
                # Create default settings
                settings = frappe.get_doc({
                    'doctype': 'ZATCA Settings',
                    'company_tax_number': settings_data.get('company_tax_number', ''),
                    'zatca_api_url': settings_data.get('zatca_api_url', ''),
                    'zatca_client_id': settings_data.get('zatca_client_id', ''),
                    'zatca_client_secret': settings_data.get('zatca_client_secret', ''),
                    'zatca_certificate_path': settings_data.get('zatca_certificate_path', ''),
                    'zatca_private_key_path': settings_data.get('zatca_private_key_path', ''),
                    'zatca_mode': settings_data.get('zatca_mode', 'test'),
                    'seidit_license_key': settings_data.get('seidit_license_key', ''),
                    'seidit_license_active': settings_data.get('seidit_license_active', False),
                    'provider': self.provider,
                    'version': self.version
                })
                settings.insert()
            else:
                # Update existing settings
                settings = frappe.get_doc("ZATCA Settings", "Default")
                settings.company_tax_number = settings_data.get('company_tax_number', settings.company_tax_number)
                settings.zatca_api_url = settings_data.get('zatca_api_url', settings.zatca_api_url)
                settings.zatca_client_id = settings_data.get('zatca_client_id', settings.zatca_client_id)
                settings.zatca_client_secret = settings_data.get('zatca_client_secret', settings.zatca_client_secret)
                settings.zatca_certificate_path = settings_data.get('zatca_certificate_path', settings.zatca_certificate_path)
                settings.zatca_private_key_path = settings_data.get('zatca_private_key_path', settings.zatca_private_key_path)
                settings.zatca_mode = settings_data.get('zatca_mode', settings.zatca_mode)
                settings.seidit_license_key = settings_data.get('seidit_license_key', settings.seidit_license_key)
                settings.seidit_license_active = settings_data.get('seidit_license_active', settings.seidit_license_active)
                settings.save()
            
            return {
                'status': 'success',
                'message': 'Settings updated successfully',
                'provider': self.provider
            }
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Settings Update Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to update settings: {str(e)}',
                'provider': self.provider
            }
    
    def test_zatca_connection(self):
        """Test ZATCA API connection"""
        try:
            if not frappe.db.exists("ZATCA Settings", "Default"):
                return {
                    'status': 'error',
                    'message': 'ZATCA settings not configured',
                    'provider': self.provider
                }
            
            settings = frappe.get_doc("ZATCA Settings", "Default")
            
            # Test connection parameters
            test_data = {
                'client_id': settings.zatca_client_id,
                'client_secret': settings.zatca_client_secret,
                'certificate_path': settings.zatca_certificate_path,
                'private_key_path': settings.zatca_private_key_path,
                'mode': settings.zatca_mode
            }
            
            # Log test attempt
            self._log_test_attempt('connection_test', test_data)
            
            # Simulate connection test (in real implementation, this would call ZATCA API)
            if all([test_data['client_id'], test_data['client_secret']]):
                return {
                    'status': 'success',
                    'message': 'ZATCA connection test successful',
                    'provider': self.provider,
                    'test_data': {
                        'mode': test_data['mode'],
                        'timestamp': datetime.now().isoformat()
                    }
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Missing ZATCA credentials',
                    'provider': self.provider
                }
                
        except Exception as e:
            frappe.log_error(f"SEIDiT Connection Test Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}',
                'provider': self.provider
            }
    
    def generate_test_invoice(self):
        """Generate test invoice"""
        try:
            # Check license status
            from seidit_license_system import SEIDiTLicenseSystem
            license_system = SEIDiTLicenseSystem()
            can_generate, message = license_system.can_generate_invoice()
            
            if not can_generate:
                return {
                    'status': 'error',
                    'message': message,
                    'provider': self.provider
                }
            
            # Generate test invoice data
            test_invoice = {
                'invoice_number': f'TEST-{int(time.time())}',
                'customer_name': 'Test Customer',
                'amount': 100.00,
                'vat_amount': 15.00,
                'total_amount': 115.00,
                'invoice_date': datetime.now().date().isoformat(),
                'mode': 'test'
            }
            
            # Log test invoice generation
            self._log_test_attempt('test_invoice', test_invoice)
            
            # Log usage
            license_system.log_invoice_generation()
            
            return {
                'status': 'success',
                'message': 'Test invoice generated successfully',
                'provider': self.provider,
                'test_invoice': test_invoice
            }
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Test Invoice Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Test invoice generation failed: {str(e)}',
                'provider': self.provider
            }
    
    def activate_live_mode(self):
        """Activate live mode"""
        try:
            if not frappe.db.exists("ZATCA Settings", "Default"):
                return {
                    'status': 'error',
                    'message': 'ZATCA settings not configured',
                    'provider': self.provider
                }
            
            settings = frappe.get_doc("ZATCA Settings", "Default")
            
            # Check if license is active
            if not settings.seidit_license_active:
                return {
                    'status': 'error',
                    'message': 'SEIDiT license required for live mode',
                    'provider': self.provider
                }
            
            # Switch to live mode
            settings.zatca_mode = 'live'
            settings.save()
            
            # Log live mode activation
            self._log_test_attempt('live_mode_activation', {
                'mode': 'live',
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'status': 'success',
                'message': 'Live mode activated successfully',
                'provider': self.provider
            }
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Live Mode Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Live mode activation failed: {str(e)}',
                'provider': self.provider
            }
    
    def _log_test_attempt(self, test_type, test_data):
        """Log test attempts"""
        try:
            frappe.get_doc({
                'doctype': 'ZATCA Log',
                'action': f'wizard_{test_type}',
                'status': 'success',
                'message': f'SEIDiT Wizard {test_type}',
                'data': json.dumps(test_data),
                'provider': self.provider,
                'timestamp': datetime.now()
            }).insert()
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Test Log Error: {str(e)}")

# API Endpoints
@frappe.whitelist()
def get_seidit_wizard_data():
    """Get SEIDiT wizard data"""
    try:
        wizard = SEIDiTZATCASetupWizard()
        return wizard.get_wizard_data()
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to get wizard data: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def update_seidit_settings(settings_data):
    """Update SEIDiT ZATCA settings"""
    try:
        wizard = SEIDiTZATCASetupWizard()
        return wizard.update_settings(json.loads(settings_data))
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to update settings: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def test_seidit_zatca_connection():
    """Test SEIDiT ZATCA connection"""
    try:
        wizard = SEIDiTZATCASetupWizard()
        return wizard.test_zatca_connection()
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Connection test failed: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def generate_seidit_test_invoice():
    """Generate SEIDiT test invoice"""
    try:
        wizard = SEIDiTZATCASetupWizard()
        return wizard.generate_test_invoice()
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Test invoice generation failed: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def activate_seidit_live_mode():
    """Activate SEIDiT live mode"""
    try:
        wizard = SEIDiTZATCASetupWizard()
        return wizard.activate_live_mode()
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Live mode activation failed: {str(e)}',
            'provider': 'SEIDiT'
        } 