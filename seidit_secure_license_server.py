"""
SEIDiT Secure License Server
============================

Secure server-side license validation system for SEIDiT ZATCA module.
This prevents reverse engineering and ensures only valid licenses work.

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.
"""

import hashlib
import hmac
import base64
import json
import time
import uuid
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import requests
import frappe

class SEIDiTSecureLicenseServer:
    """
    SEIDiT Secure License Server
    
    Server-side license validation with:
    - Remote license verification
    - Anti-reverse engineering protection
    - Hardware fingerprinting
    - Time-based validation
    - Encrypted communication
    """
    
    def __init__(self):
        self.server_url = "https://license.seidit.com/api/v1"
        self.api_key = "seidit_license_server_key_2024"
        self.secret_key = "seidit_license_secret_2024_secure"
        self.provider = "SEIDiT"
        self.version = "2.0.0"
        
        # Encryption keys (in production, these would be stored securely)
        self.encryption_key = self._generate_encryption_key()
        self.fernet = Fernet(self.encryption_key)
    
    def _generate_encryption_key(self):
        """Generate encryption key for license communication"""
        salt = b'seidit_license_salt_2024_secure'
        password = b'seidit_license_password_2024_secure'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def generate_secure_license(self, installation_id, customer_info):
        """Generate secure license with server-side validation"""
        try:
            license_data = {
                'installation_id': installation_id,
                'customer_info': customer_info,
                'provider': self.provider,
                'version': self.version,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=365*10)).isoformat(),  # 10 years
                'license_type': 'lifetime',
                'features': ['zatca_compliance', 'unlimited_invoices', 'premium_support'],
                'signature': None  # Will be added by server
            }
            
            # Create signature
            signature_data = {
                'installation_id': installation_id,
                'provider': self.provider,
                'version': self.version,
                'created_at': license_data['created_at']
            }
            
            signature_string = json.dumps(signature_data, sort_keys=True)
            license_data['signature'] = hmac.new(
                self.secret_key.encode(),
                signature_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Encrypt license data
            encrypted_data = self.fernet.encrypt(json.dumps(license_data).encode())
            license_key = base64.urlsafe_b64encode(encrypted_data).decode()
            
            return {
                'status': 'success',
                'license_key': license_key,
                'installation_id': installation_id,
                'provider': self.provider
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'License generation failed: {str(e)}'
            }
    
    def validate_license_remotely(self, license_key, installation_id):
        """Validate license with server-side verification"""
        try:
            # Decrypt license data
            encrypted_data = base64.urlsafe_b64decode(license_key.encode())
            decrypted_data = self.fernet.decrypt(encrypted_data)
            license_data = json.loads(decrypted_data.decode())
            
            # Verify installation ID
            if license_data.get('installation_id') != installation_id:
                return False, "License not valid for this installation"
            
            # Verify signature
            signature_data = {
                'installation_id': license_data['installation_id'],
                'provider': license_data['provider'],
                'version': license_data['version'],
                'created_at': license_data['created_at']
            }
            
            expected_signature = hmac.new(
                self.secret_key.encode(),
                json.dumps(signature_data, sort_keys=True).encode(),
                hashlib.sha256
            ).hexdigest()
            
            if license_data.get('signature') != expected_signature:
                return False, "Invalid license signature"
            
            # Check expiration
            expires_at = datetime.fromisoformat(license_data['expires_at'])
            if datetime.now() > expires_at:
                return False, "License has expired"
            
            # Remote server validation
            server_response = self._validate_with_server(license_key, installation_id)
            if not server_response.get('valid'):
                return False, server_response.get('message', 'Server validation failed')
            
            return True, "License is valid"
            
        except Exception as e:
            return False, f"License validation error: {str(e)}"
    
    def _validate_with_server(self, license_key, installation_id):
        """Validate license with SEIDiT license server"""
        try:
            # This would be a real API call to SEIDiT's license server
            # For demo purposes, we'll simulate the server response
            
            payload = {
                'license_key': license_key,
                'installation_id': installation_id,
                'timestamp': int(time.time()),
                'provider': self.provider
            }
            
            # Create request signature
            signature = hmac.new(
                self.api_key.encode(),
                json.dumps(payload, sort_keys=True).encode(),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'Content-Type': 'application/json',
                'X-SEIDiT-Signature': signature,
                'X-SEIDiT-Provider': self.provider,
                'User-Agent': f'SEIDiT-License-Client/{self.version}'
            }
            
            # In production, this would be a real API call
            # For now, we'll simulate the response
            if self._is_valid_license_locally(license_key, installation_id):
                return {
                    'valid': True,
                    'message': 'License validated successfully',
                    'server_timestamp': int(time.time())
                }
            else:
                return {
                    'valid': False,
                    'message': 'License not found in server database'
                }
                
        except Exception as e:
            return {
                'valid': False,
                'message': f'Server validation error: {str(e)}'
            }
    
    def _is_valid_license_locally(self, license_key, installation_id):
        """Check if license is valid locally (simulates server database)"""
        # In production, this would check against a real database
        # For demo purposes, we'll use a simple check
        
        # Extract installation ID from license
        try:
            encrypted_data = base64.urlsafe_b64decode(license_key.encode())
            decrypted_data = self.fernet.decrypt(encrypted_data)
            license_data = json.loads(decrypted_data.decode())
            
            return license_data.get('installation_id') == installation_id
        except:
            return False
    
    def revoke_license(self, license_key, installation_id):
        """Revoke license (server-side)"""
        try:
            payload = {
                'license_key': license_key,
                'installation_id': installation_id,
                'action': 'revoke',
                'timestamp': int(time.time()),
                'provider': self.provider
            }
            
            signature = hmac.new(
                self.api_key.encode(),
                json.dumps(payload, sort_keys=True).encode(),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'Content-Type': 'application/json',
                'X-SEIDiT-Signature': signature,
                'X-SEIDiT-Provider': self.provider
            }
            
            # In production, this would be a real API call
            return {
                'status': 'success',
                'message': 'License revoked successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'License revocation failed: {str(e)}'
            }

class SEIDiTSecureLicenseClient:
    """
    SEIDiT Secure License Client
    
    Client-side license validation with anti-reverse engineering protection
    """
    
    def __init__(self):
        self.provider = "SEIDiT"
        self.version = "2.0.0"
        self.license_server = SEIDiTSecureLicenseServer()
        
    def validate_license(self, license_key, installation_id):
        """Validate license with anti-reverse engineering protection"""
        try:
            # Anti-reverse engineering checks
            if not self._check_environment():
                return False, "Environment validation failed"
            
            # Validate license remotely
            is_valid, message = self.license_server.validate_license_remotely(license_key, installation_id)
            
            if is_valid:
                # Update local license status
                self._update_license_status(license_key, installation_id, True)
                return True, "License validated successfully"
            else:
                self._update_license_status(license_key, installation_id, False)
                return False, message
                
        except Exception as e:
            return False, f"License validation error: {str(e)}"
    
    def _check_environment(self):
        """Anti-reverse engineering environment checks"""
        try:
            # Check for debugging tools
            import sys
            if hasattr(sys, 'gettrace') and sys.gettrace():
                return False
            
            # Check for common reverse engineering tools
            suspicious_modules = ['idaapi', 'x64dbg', 'ollydbg', 'ghidra']
            for module in suspicious_modules:
                try:
                    __import__(module)
                    return False
                except ImportError:
                    pass
            
            # Check for virtualization
            try:
                import psutil
                for proc in psutil.process_iter(['name']):
                    if any(tool in proc.info['name'].lower() for tool in ['vmware', 'vbox', 'qemu']):
                        return False
            except:
                pass
            
            return True
            
        except Exception:
            return False
    
    def _update_license_status(self, license_key, installation_id, is_valid):
        """Update local license status"""
        try:
            if frappe.db.exists("ZATCA Settings", "Default"):
                settings = frappe.get_doc("ZATCA Settings", "Default")
                settings.seidit_license_key = license_key if is_valid else ""
                settings.seidit_license_active = is_valid
                settings.seidit_license_validated_at = datetime.now()
                settings.save()
        except Exception as e:
            frappe.log_error(f"SEIDiT License Status Update Error: {str(e)}")
    
    def get_license_info(self, license_key):
        """Get license information"""
        try:
            encrypted_data = base64.urlsafe_b64decode(license_key.encode())
            decrypted_data = self.license_server.fernet.decrypt(encrypted_data)
            license_data = json.loads(decrypted_data.decode())
            
            return {
                'installation_id': license_data.get('installation_id'),
                'provider': license_data.get('provider'),
                'version': license_data.get('version'),
                'created_at': license_data.get('created_at'),
                'expires_at': license_data.get('expires_at'),
                'license_type': license_data.get('license_type'),
                'features': license_data.get('features', [])
            }
        except Exception as e:
            return None

# API Endpoints for secure licensing
@frappe.whitelist()
def validate_seidit_secure_license(license_key):
    """Validate SEIDiT license with secure server validation"""
    try:
        from seidit_license_system import SEIDiTLicenseSystem
        license_system = SEIDiTLicenseSystem()
        installation_info = license_system.get_installation_info()
        installation_id = installation_info.get('installation_id')
        
        client = SEIDiTSecureLicenseClient()
        is_valid, message = client.validate_license(license_key, installation_id)
        
        return {
            'valid': is_valid,
            'message': message,
            'provider': 'SEIDiT',
            'installation_id': installation_id
        }
        
    except Exception as e:
        return {
            'valid': False,
            'message': f'License validation error: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def get_seidit_license_info(license_key):
    """Get SEIDiT license information"""
    try:
        client = SEIDiTSecureLicenseClient()
        license_info = client.get_license_info(license_key)
        
        if license_info:
            return {
                'status': 'success',
                'license_info': license_info,
                'provider': 'SEIDiT'
            }
        else:
            return {
                'status': 'error',
                'message': 'Invalid license key',
                'provider': 'SEIDiT'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error getting license info: {str(e)}',
            'provider': 'SEIDiT'
        }

# Server-side license generation (for SEIDiT use only)
@frappe.whitelist()
def generate_seidit_license(installation_id, customer_info):
    """Generate SEIDiT license (server-side only)"""
    try:
        # This should only be accessible by SEIDiT administrators
        if not frappe.has_permission("System Manager"):
            return {
                'status': 'error',
                'message': 'Unauthorized access',
                'provider': 'SEIDiT'
            }
        
        server = SEIDiTSecureLicenseServer()
        result = server.generate_secure_license(installation_id, customer_info)
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'License generation error: {str(e)}',
            'provider': 'SEIDiT'
        } 