"""
SEIDiT ZATCA Phase 2 Licensing System
======================================

Intelligent licensing system for SEIDiT ZATCA module with:
- Installation tracking
- Anti-reuse protection
- Hardware fingerprinting
- License validation
- Usage monitoring

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.
"""

import frappe
import hashlib
import uuid
import json
import platform
import socket
import psutil
import requests
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SEIDiTLicenseSystem:
    """
    SEIDiT Intelligent Licensing System
    
    Features:
    - Unique installation ID generation
    - Hardware fingerprinting
    - Anti-reuse protection
    - License validation
    - Usage monitoring
    - One-time use enforcement
    """
    
    def __init__(self):
        self.provider = "SEIDiT"
        self.website = "https://seidit.com"
        self.support_email = "zatca@seidit.com"
        self.support_whatsapp = "+966567414356"
        self.version = "2.0.0"
        self.free_limit = 10  # Maximum free invoices
        self.license_key = None
        self.installation_id = None
        
    def generate_installation_id(self):
        """Generate unique installation ID based on hardware and site fingerprint"""
        try:
            # Get system information
            system_info = {
                'hostname': socket.gethostname(),
                'platform': platform.platform(),
                'processor': platform.processor(),
                'machine': platform.machine(),
                'site_name': frappe.local.site,
                'site_path': frappe.get_app_path('erpnext'),
                'timestamp': datetime.now().isoformat()
            }
            
            # Get hardware fingerprint
            cpu_info = platform.processor()
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')
            
            hardware_fingerprint = {
                'cpu_count': psutil.cpu_count(),
                'memory_total': memory_info.total,
                'disk_total': disk_info.total,
                'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
                'network_interfaces': self._get_network_interfaces()
            }
            
            # Combine all information
            fingerprint_data = {
                'system': system_info,
                'hardware': hardware_fingerprint,
                'site': {
                    'name': frappe.local.site,
                    'path': frappe.get_app_path('erpnext'),
                    'db_name': frappe.conf.db_name
                }
            }
            
            # Generate unique installation ID
            fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
            installation_id = hashlib.sha256(fingerprint_string.encode()).hexdigest()[:16].upper()
            
            return installation_id, fingerprint_data
            
        except Exception as e:
            frappe.log_error(f"SEIDiT License Error: {str(e)}")
            return None, None
    
    def _get_network_interfaces(self):
        """Get network interface information for fingerprinting"""
        try:
            interfaces = {}
            for interface, addresses in psutil.net_if_addrs().items():
                interfaces[interface] = []
                for addr in addresses:
                    interfaces[interface].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask
                    })
            return interfaces
        except:
            return {}
    
    def get_installation_info(self):
        """Get current installation information"""
        installation_id, fingerprint = self.generate_installation_id()
        
        return {
            'installation_id': installation_id,
            'site_name': frappe.local.site,
            'site_path': frappe.get_app_path('erpnext'),
            'system_info': {
                'hostname': socket.gethostname(),
                'platform': platform.platform(),
                'processor': platform.processor()
            },
            'hardware_info': {
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'disk_total': psutil.disk_usage('/').total
            },
            'timestamp': datetime.now().isoformat(),
            'provider': self.provider,
            'version': self.version
        }
    
    def validate_license(self, license_key):
        """Validate SEIDiT license key with anti-reuse protection"""
        try:
            if not license_key:
                return False, "License key is required"
            
            # Decode and validate license
            decoded_license = self._decode_license(license_key)
            if not decoded_license:
                return False, "Invalid license format"
            
            # Check license structure
            if not self._validate_license_structure(decoded_license):
                return False, "Invalid license structure"
            
            # Get current installation info
            current_installation = self.get_installation_info()
            
            # Check if license is bound to this installation
            if decoded_license.get('installation_id') != current_installation['installation_id']:
                return False, "License is not valid for this installation"
            
            # Check if license is already used
            if self._is_license_used(license_key):
                return False, "License has already been used on another installation"
            
            # Validate license signature
            if not self._validate_license_signature(decoded_license):
                return False, "License signature validation failed"
            
            # Mark license as used for this installation
            self._mark_license_used(license_key, current_installation['installation_id'])
            
            return True, "License validated successfully"
            
        except Exception as e:
            frappe.log_error(f"SEIDiT License Validation Error: {str(e)}")
            return False, f"License validation error: {str(e)}"
    
    def _decode_license(self, license_key):
        """Decode SEIDiT license key"""
        try:
            # Remove any formatting
            clean_key = license_key.replace('-', '').replace(' ', '')
            
            # Decode base64
            decoded = base64.b64decode(clean_key)
            
            # Decrypt license data
            key = self._get_license_key()
            fernet = Fernet(key)
            decrypted = fernet.decrypt(decoded)
            
            return json.loads(decrypted.decode())
            
        except Exception as e:
            frappe.log_error(f"SEIDiT License Decode Error: {str(e)}")
            return None
    
    def _get_license_key(self):
        """Get SEIDiT license encryption key"""
        # This would be a secret key known only to SEIDiT
        # In production, this should be stored securely
        salt = b'seidit_zatca_license_salt_2024'
        password = b'seidit_zatca_license_secret_key_2024'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def _validate_license_structure(self, license_data):
        """Validate license data structure"""
        required_fields = ['installation_id', 'provider', 'version', 'signature', 'timestamp']
        
        for field in required_fields:
            if field not in license_data:
                return False
        
        if license_data.get('provider') != self.provider:
            return False
        
        return True
    
    def _validate_license_signature(self, license_data):
        """Validate license signature"""
        try:
            # Create signature from license data
            signature_data = {
                'installation_id': license_data['installation_id'],
                'provider': license_data['provider'],
                'version': license_data['version'],
                'timestamp': license_data['timestamp']
            }
            
            signature_string = json.dumps(signature_data, sort_keys=True)
            expected_signature = hashlib.sha256(signature_string.encode()).hexdigest()
            
            return license_data['signature'] == expected_signature
            
        except Exception as e:
            frappe.log_error(f"SEIDiT License Signature Error: {str(e)}")
            return False
    
    def _is_license_used(self, license_key):
        """Check if license is already used on another installation"""
        try:
            # Check in database
            used_licenses = frappe.get_all('SEIDiT License Usage', 
                filters={'license_key': license_key},
                fields=['installation_id', 'used_at'])
            
            if used_licenses:
                current_installation = self.get_installation_info()
                for used_license in used_licenses:
                    if used_license['installation_id'] != current_installation['installation_id']:
                        return True
            
            return False
            
        except Exception as e:
            frappe.log_error(f"SEIDiT License Usage Check Error: {str(e)}")
            return False
    
    def _mark_license_used(self, license_key, installation_id):
        """Mark license as used for this installation"""
        try:
            # Create license usage record
            frappe.get_doc({
                'doctype': 'SEIDiT License Usage',
                'license_key': license_key,
                'installation_id': installation_id,
                'used_at': datetime.now(),
                'site_name': frappe.local.site,
                'provider': self.provider
            }).insert()
            
        except Exception as e:
            frappe.log_error(f"SEIDiT License Usage Mark Error: {str(e)}")
    
    def check_usage_limit(self):
        """Check if usage is within free limit"""
        try:
            # Count processed invoices
            processed_invoices = frappe.get_all('Sales Invoice',
                filters={
                    'zatca_status': ['in', ['success', 'processing']],
                    'zatca_provider': 'SEIDiT'
                },
                fields=['name'])
            
            invoice_count = len(processed_invoices)
            
            # Check if license is active
            license_active = self._is_license_active()
            
            if license_active:
                return True, "License active - unlimited usage"
            else:
                if invoice_count < self.free_limit:
                    return True, f"Free usage: {invoice_count}/{self.free_limit} invoices"
                else:
                    return False, f"Free limit reached: {invoice_count}/{self.free_limit} invoices"
                    
        except Exception as e:
            frappe.log_error(f"SEIDiT Usage Check Error: {str(e)}")
            return False, "Error checking usage limit"
    
    def _is_license_active(self):
        """Check if SEIDiT license is active"""
        try:
            settings = frappe.get_doc("ZATCA Settings")
            if settings.get('seidit_license_key'):
                is_valid, message = self.validate_license(settings.seidit_license_key)
                return is_valid
            return False
            
        except Exception as e:
            frappe.log_error(f"SEIDiT License Active Check Error: {str(e)}")
            return False
    
    def get_license_status(self):
        """Get current license status"""
        try:
            installation_info = self.get_installation_info()
            usage_ok, usage_message = self.check_usage_limit()
            license_active = self._is_license_active()
            
            return {
                'installation_id': installation_info['installation_id'],
                'site_name': installation_info['site_name'],
                'license_active': license_active,
                'usage_ok': usage_ok,
                'usage_message': usage_message,
                'free_limit': self.free_limit,
                'provider': self.provider,
                'version': self.version,
                'support_email': self.support_email,
                'support_whatsapp': self.support_whatsapp
            }
            
        except Exception as e:
            frappe.log_error(f"SEIDiT License Status Error: {str(e)}")
            return None

# API Endpoints for SEIDiT License System
@frappe.whitelist()
def get_seidit_license_status():
    """Get SEIDiT license status"""
    license_system = SEIDiTLicenseSystem()
    return license_system.get_license_status()

@frappe.whitelist()
def validate_seidit_license(license_key):
    """Validate SEIDiT license key"""
    license_system = SEIDiTLicenseSystem()
    is_valid, message = license_system.validate_license(license_key)
    
    if is_valid:
        # Update settings with valid license
        settings = frappe.get_doc("ZATCA Settings")
        settings.seidit_license_key = license_key
        settings.seidit_license_active = True
        settings.save()
    
    return {
        'valid': is_valid,
        'message': message,
        'provider': 'SEIDiT'
    }

@frappe.whitelist()
def get_seidit_installation_info():
    """Get SEIDiT installation information"""
    license_system = SEIDiTLicenseSystem()
    return license_system.get_installation_info()

# License usage tracking
def track_invoice_processing(invoice_name):
    """Track invoice processing for license usage"""
    try:
        license_system = SEIDiTLicenseSystem()
        usage_ok, message = license_system.check_usage_limit()
        
        if not usage_ok:
            frappe.throw(f"SEIDiT License Limit: {message}. Please contact {license_system.support_email} for license.")
        
        # Log usage
        frappe.get_doc({
            'doctype': 'SEIDiT Usage Log',
            'invoice': invoice_name,
            'usage_type': 'invoice_processing',
            'timestamp': datetime.now(),
            'provider': 'SEIDiT'
        }).insert()
        
    except Exception as e:
        frappe.log_error(f"SEIDiT Usage Tracking Error: {str(e)}") 