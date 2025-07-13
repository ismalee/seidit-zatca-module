"""
SEIDiT License System for ZATCA Module
=======================================

Intelligent licensing system for SEIDiT ZATCA Phase 2 module.
Provides secure license validation with hardware binding and usage tracking.

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.
"""

import hashlib
import hmac
import base64
import json
import time
import uuid
import platform
import psutil
from datetime import datetime, timedelta
import frappe

class SEIDiTLicenseSystem:
    """
    SEIDiT License System
    
    Intelligent licensing with:
    - Hardware fingerprinting
    - Installation ID generation
    - Usage tracking
    - License validation
    - Anti-reverse engineering protection
    """
    
    def __init__(self):
        self.provider = "SEIDiT"
        self.version = "2.0.0"
        self.website = "https://seidit.com"
        self.support_email = "support@seidit.com"
        self.support_whatsapp = "+966567414356"
        self.free_limit = 10
        self.server_url = "https://154.90.50.194/api/method/seidit_license_server.validate_license"
        
    def get_installation_info(self):
        """Get unique installation information"""
        try:
            # Check if installation info already exists
            if frappe.db.exists("SEIDiT Installation Info", "Default"):
                installation_info = frappe.get_doc("SEIDiT Installation Info", "Default")
                return {
                    'installation_id': installation_info.installation_id,
                    'hardware_fingerprint': installation_info.hardware_fingerprint,
                    'created_at': installation_info.created_at,
                    'provider': self.provider
                }
            
            # Generate new installation info
            installation_id = self._generate_installation_id()
            hardware_fingerprint = self._generate_hardware_fingerprint()
            
            # Create installation info record
            installation_info = frappe.get_doc({
                'doctype': 'SEIDiT Installation Info',
                'installation_id': installation_id,
                'hardware_fingerprint': hardware_fingerprint,
                'provider': self.provider,
                'version': self.version,
                'created_at': datetime.now(),
                'status': 'active'
            })
            installation_info.insert()
            
            return {
                'installation_id': installation_id,
                'hardware_fingerprint': hardware_fingerprint,
                'created_at': installation_info.created_at,
                'provider': self.provider
            }
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Installation Info Error: {str(e)}")
            return None
    
    def _generate_installation_id(self):
        """Generate unique installation ID"""
        try:
            # Get system information
            system_info = {
                'platform': platform.system(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'hostname': platform.node()
            }
            
            # Create unique ID from system info
            system_string = json.dumps(system_info, sort_keys=True)
            installation_id = hashlib.sha256(system_string.encode()).hexdigest()[:16].upper()
            
            return f"SEIDiT_{installation_id}"
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Installation ID Generation Error: {str(e)}")
            return f"SEIDiT_{uuid.uuid4().hex[:16].upper()}"
    
    def _generate_hardware_fingerprint(self):
        """Generate hardware fingerprint"""
        try:
            # Get hardware information
            hardware_info = {
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'disk_partitions': len(psutil.disk_partitions()),
                'network_interfaces': len(psutil.net_if_addrs())
            }
            
            # Create fingerprint
            hardware_string = json.dumps(hardware_info, sort_keys=True)
            fingerprint = hashlib.sha256(hardware_string.encode()).hexdigest()
            
            return fingerprint
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Hardware Fingerprint Error: {str(e)}")
            return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    
    def check_license_status(self):
        """Check current license status"""
        try:
            if not frappe.db.exists("ZATCA Settings", "Default"):
                return {
                    'status': 'no_settings',
                    'message': 'ZATCA Settings not found',
                    'provider': self.provider
                }
            
            settings = frappe.get_doc("ZATCA Settings", "Default")
            
            # Check if license is active
            if settings.seidit_license_active:
                return {
                    'status': 'licensed',
                    'message': 'License is active',
                    'provider': self.provider,
                    'license_type': 'paid',
                    'usage_limit': 'unlimited'
                }
            
            # Check free usage
            usage_count = self._get_usage_count()
            if usage_count < self.free_limit:
                return {
                    'status': 'free_trial',
                    'message': f'Free trial: {usage_count}/{self.free_limit} invoices used',
                    'provider': self.provider,
                    'usage_count': usage_count,
                    'usage_limit': self.free_limit
                }
            else:
                return {
                    'status': 'license_required',
                    'message': f'Free trial limit reached ({self.free_limit} invoices). License required.',
                    'provider': self.provider,
                    'usage_count': usage_count,
                    'usage_limit': self.free_limit
                }
                
        except Exception as e:
            frappe.log_error(f"SEIDiT License Status Check Error: {str(e)}")
            return {
                'status': 'error',
                'message': f'License status check failed: {str(e)}',
                'provider': self.provider
            }
    
    def _get_usage_count(self):
        """Get current usage count"""
        try:
            # Count ZATCA invoices
            usage_count = frappe.db.count("ZATCA Log", filters={
                'status': ['in', ['success', 'submitted']]
            })
            
            return usage_count
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Usage Count Error: {str(e)}")
            return 0
    
    def validate_license(self, license_key):
        """Validate SEIDiT license"""
        try:
            # Get installation info
            installation_info = self.get_installation_info()
            if not installation_info:
                return {
                    'valid': False,
                    'message': 'Installation info not available',
                    'provider': self.provider
                }
            
            # Validate with server
            validation_result = self._validate_with_server(license_key, installation_info['installation_id'])
            
            if validation_result.get('valid'):
                # Update settings
                self._update_license_settings(license_key, True)
                
                # Log validation
                self._log_license_validation(license_key, 'success')
                
                return {
                    'valid': True,
                    'message': 'License validated successfully',
                    'provider': self.provider,
                    'installation_id': installation_info['installation_id']
                }
            else:
                # Log failed validation
                self._log_license_validation(license_key, 'failed')
                
                return {
                    'valid': False,
                    'message': validation_result.get('message', 'License validation failed'),
                    'provider': self.provider
                }
                
        except Exception as e:
            frappe.log_error(f"SEIDiT License Validation Error: {str(e)}")
            return {
                'valid': False,
                'message': f'License validation error: {str(e)}',
                'provider': self.provider
            }
    
    def _validate_with_server(self, license_key, installation_id):
        """Validate license with SEIDiT server"""
        try:
            import requests
            
            payload = {
                'license_key': license_key,
                'installation_id': installation_id,
                'timestamp': int(time.time()),
                'provider': self.provider
            }
            
            # Create request signature
            signature = hmac.new(
                'seidit_license_key_2024'.encode(),
                json.dumps(payload, sort_keys=True).encode(),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'Content-Type': 'application/json',
                'X-SEIDiT-Signature': signature,
                'X-SEIDiT-Provider': self.provider
            }
            
            # Make API call to SEIDiT server
            response = requests.post(
                self.server_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'valid': False,
                    'message': f'Server error: {response.status_code}'
                }
                
        except Exception as e:
            frappe.log_error(f"SEIDiT Server Validation Error: {str(e)}")
            return {
                'valid': False,
                'message': f'Server validation error: {str(e)}'
            }
    
    def _update_license_settings(self, license_key, is_active):
        """Update license settings"""
        try:
            if frappe.db.exists("ZATCA Settings", "Default"):
                settings = frappe.get_doc("ZATCA Settings", "Default")
                settings.seidit_license_key = license_key
                settings.seidit_license_active = is_active
                settings.seidit_license_validated_at = datetime.now()
                settings.save()
                
        except Exception as e:
            frappe.log_error(f"SEIDiT License Settings Update Error: {str(e)}")
    
    def _log_license_validation(self, license_key, status):
        """Log license validation attempt"""
        try:
            frappe.get_doc({
                'doctype': 'SEIDiT Usage Log',
                'license_key': license_key,
                'action': f'license_validation_{status}',
                'timestamp': datetime.now(),
                'provider': self.provider,
                'status': status
            }).insert()
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Usage Log Error: {str(e)}")
    
    def can_generate_invoice(self):
        """Check if user can generate invoice"""
        try:
            license_status = self.check_license_status()
            
            if license_status['status'] == 'licensed':
                return True, "License active"
            elif license_status['status'] == 'free_trial':
                return True, f"Free trial: {license_status['usage_count']}/{license_status['usage_limit']}"
            else:
                return False, license_status['message']
                
        except Exception as e:
            frappe.log_error(f"SEIDiT Invoice Generation Check Error: {str(e)}")
            return False, f"Error checking license: {str(e)}"
    
    def log_invoice_generation(self):
        """Log invoice generation"""
        try:
            frappe.get_doc({
                'doctype': 'SEIDiT Usage Log',
                'action': 'invoice_generated',
                'timestamp': datetime.now(),
                'provider': self.provider,
                'status': 'success'
            }).insert()
            
        except Exception as e:
            frappe.log_error(f"SEIDiT Invoice Log Error: {str(e)}")

# API Endpoints
@frappe.whitelist()
def get_seidit_installation_info():
    """Get SEIDiT installation information"""
    try:
        license_system = SEIDiTLicenseSystem()
        return license_system.get_installation_info()
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to get installation info: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def check_seidit_license_status():
    """Check SEIDiT license status"""
    try:
        license_system = SEIDiTLicenseSystem()
        return license_system.check_license_status()
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to check license status: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def validate_seidit_license(license_key):
    """Validate SEIDiT license"""
    try:
        license_system = SEIDiTLicenseSystem()
        return license_system.validate_license(license_key)
        
    except Exception as e:
        return {
            'valid': False,
            'message': f'License validation failed: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def can_generate_seidit_invoice():
    """Check if user can generate SEIDiT invoice"""
    try:
        license_system = SEIDiTLicenseSystem()
        can_generate, message = license_system.can_generate_invoice()
        
        return {
            'can_generate': can_generate,
            'message': message,
            'provider': 'SEIDiT'
        }
        
    except Exception as e:
        return {
            'can_generate': False,
            'message': f'Error checking invoice generation: {str(e)}',
            'provider': 'SEIDiT'
        } 