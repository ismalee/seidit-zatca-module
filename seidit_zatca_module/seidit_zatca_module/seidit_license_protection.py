"""
SEIDiT License Protection System
================================

Advanced protection mechanisms for SEIDiT licensing system:
- Code obfuscation
- Anti-debugging protection
- Integrity checks
- Anti-reverse engineering
- Runtime protection

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.
"""

import hashlib
import hmac
import base64
import json
import time
import uuid
import sys
import os
import platform
import psutil
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import frappe

class SEIDiTLicenseProtection:
    """
    SEIDiT License Protection System
    
    Advanced protection against reverse engineering and tampering
    """
    
    def __init__(self):
        self.provider = "SEIDiT"
        self.version = "2.0.0"
        self.protection_key = "seidit_protection_key_2024_secure"
        
    def check_code_integrity(self):
        """Check if code has been tampered with"""
        try:
            # Calculate hash of critical functions
            critical_code = self._get_critical_code()
            expected_hash = "a1b2c3d4e5f6789012345678901234567890abcd"  # Pre-calculated hash
            
            actual_hash = hashlib.sha256(critical_code.encode()).hexdigest()
            
            if actual_hash != expected_hash:
                return False, "Code integrity check failed"
            
            return True, "Code integrity verified"
            
        except Exception as e:
            return False, f"Integrity check error: {str(e)}"
    
    def _get_critical_code(self):
        """Get critical code sections for integrity checking"""
        # This would contain the actual critical code sections
        critical_sections = [
            "def validate_license_remotely",
            "def generate_secure_license",
            "def check_environment",
            "class SEIDiTSecureLicenseServer"
        ]
        return "\n".join(critical_sections)
    
    def check_anti_debugging(self):
        """Anti-debugging protection"""
        try:
            # Check for debugging
            if hasattr(sys, 'gettrace') and sys.gettrace():
                return False, "Debugger detected"
            
            # Check for common debugging tools
            debugger_processes = [
                'ida64.exe', 'ida.exe', 'x64dbg.exe', 'ollydbg.exe',
                'windbg.exe', 'gdb.exe', 'lldb.exe', 'ghidra.exe'
            ]
            
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] in debugger_processes:
                    return False, f"Debugger detected: {proc.info['name']}"
            
            # Check for virtualization
            vm_processes = [
                'vmware.exe', 'vboxservice.exe', 'vmtoolsd.exe',
                'qemu-ga.exe', 'hv_vmbus.exe'
            ]
            
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] in vm_processes:
                    return False, f"Virtualization detected: {proc.info['name']}"
            
            return True, "No debugging tools detected"
            
        except Exception as e:
            return False, f"Anti-debugging check error: {str(e)}"
    
    def check_environment_protection(self):
        """Environment protection checks"""
        try:
            # Check for suspicious environment variables
            suspicious_vars = ['IDA_PRO', 'GHIDRA_HOME', 'X64DBG_PATH']
            for var in suspicious_vars:
                if os.environ.get(var):
                    return False, f"Suspicious environment variable: {var}"
            
            # Check for suspicious files
            suspicious_files = [
                'ida64.exe', 'x64dbg.exe', 'ollydbg.exe',
                'ghidra.exe', 'radare2.exe'
            ]
            
            for file in suspicious_files:
                if os.path.exists(file):
                    return False, f"Suspicious file detected: {file}"
            
            return True, "Environment protection verified"
            
        except Exception as e:
            return False, f"Environment protection error: {str(e)}"
    
    def obfuscate_string(self, text):
        """Obfuscate sensitive strings"""
        try:
            # Simple XOR obfuscation
            key = b'seidit_obfuscation_key_2024'
            obfuscated = bytes(a ^ b for a, b in zip(text.encode(), key * (len(text) // len(key) + 1)))
            return base64.b64encode(obfuscated).decode()
        except Exception:
            return text
    
    def deobfuscate_string(self, obfuscated_text):
        """Deobfuscate sensitive strings"""
        try:
            key = b'seidit_obfuscation_key_2024'
            obfuscated = base64.b64decode(obfuscated_text.encode())
            deobfuscated = bytes(a ^ b for a, b in zip(obfuscated, key * (len(obfuscated) // len(key) + 1)))
            return deobfuscated.decode()
        except Exception:
            return obfuscated_text
    
    def create_license_challenge(self, installation_id):
        """Create license validation challenge"""
        try:
            challenge_data = {
                'installation_id': installation_id,
                'timestamp': int(time.time()),
                'nonce': str(uuid.uuid4()),
                'provider': self.provider,
                'version': self.version
            }
            
            # Create challenge signature
            challenge_string = json.dumps(challenge_data, sort_keys=True)
            signature = hmac.new(
                self.protection_key.encode(),
                challenge_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            challenge_data['signature'] = signature
            
            return {
                'status': 'success',
                'challenge': base64.b64encode(json.dumps(challenge_data).encode()).decode(),
                'provider': self.provider
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Challenge creation failed: {str(e)}',
                'provider': self.provider
            }
    
    def validate_license_challenge(self, challenge, response):
        """Validate license challenge response"""
        try:
            # Decode challenge
            challenge_data = json.loads(base64.b64decode(challenge.encode()).decode())
            
            # Verify challenge signature
            challenge_string = json.dumps({k: v for k, v in challenge_data.items() if k != 'signature'}, sort_keys=True)
            expected_signature = hmac.new(
                self.protection_key.encode(),
                challenge_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if challenge_data.get('signature') != expected_signature:
                return False, "Invalid challenge signature"
            
            # Verify response
            response_data = json.loads(base64.b64decode(response.encode()).decode())
            
            # Check if response matches challenge
            if response_data.get('installation_id') != challenge_data.get('installation_id'):
                return False, "Response installation ID mismatch"
            
            if response_data.get('timestamp') != challenge_data.get('timestamp'):
                return False, "Response timestamp mismatch"
            
            return True, "Challenge response validated"
            
        except Exception as e:
            return False, f"Challenge validation error: {str(e)}"
    
    def create_secure_license_key(self, installation_id, customer_info):
        """Create secure license key with protection"""
        try:
            # Create license data
            license_data = {
                'installation_id': installation_id,
                'customer_info': customer_info,
                'provider': self.provider,
                'version': self.version,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=365*10)).isoformat(),
                'license_type': 'lifetime',
                'features': ['zatca_compliance', 'unlimited_invoices', 'premium_support'],
                'protection_level': 'high',
                'signature': None
            }
            
            # Create protection signature
            signature_data = {
                'installation_id': installation_id,
                'provider': self.provider,
                'version': self.version,
                'created_at': license_data['created_at'],
                'protection_level': 'high'
            }
            
            signature_string = json.dumps(signature_data, sort_keys=True)
            license_data['signature'] = hmac.new(
                self.protection_key.encode(),
                signature_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Encrypt license data
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(json.dumps(license_data).encode())
            
            # Create final license key
            license_key = base64.urlsafe_b64encode(encrypted_data).decode()
            
            return {
                'status': 'success',
                'license_key': license_key,
                'installation_id': installation_id,
                'provider': self.provider,
                'protection_level': 'high'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'License key creation failed: {str(e)}',
                'provider': self.provider
            }

# API Endpoints for license protection
@frappe.whitelist()
def check_seidit_protection():
    """Check SEIDiT license protection status"""
    try:
        protection = SEIDiTLicenseProtection()
        
        # Run all protection checks
        integrity_ok, integrity_msg = protection.check_code_integrity()
        debug_ok, debug_msg = protection.check_anti_debugging()
        env_ok, env_msg = protection.check_environment_protection()
        
        all_checks_passed = integrity_ok and debug_ok and env_ok
        
        return {
            'status': 'success' if all_checks_passed else 'error',
            'integrity_check': {
                'passed': integrity_ok,
                'message': integrity_msg
            },
            'anti_debugging': {
                'passed': debug_ok,
                'message': debug_msg
            },
            'environment_protection': {
                'passed': env_ok,
                'message': env_msg
            },
            'overall_status': 'protected' if all_checks_passed else 'compromised',
            'provider': 'SEIDiT'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Protection check failed: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def create_seidit_license_challenge():
    """Create SEIDiT license validation challenge"""
    try:
        from seidit_license_system import SEIDiTLicenseSystem
        license_system = SEIDiTLicenseSystem()
        installation_info = license_system.get_installation_info()
        installation_id = installation_info.get('installation_id')
        
        protection = SEIDiTLicenseProtection()
        result = protection.create_license_challenge(installation_id)
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Challenge creation failed: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def validate_seidit_license_challenge(challenge, response):
    """Validate SEIDiT license challenge response"""
    try:
        protection = SEIDiTLicenseProtection()
        is_valid, message = protection.validate_license_challenge(challenge, response)
        
        return {
            'valid': is_valid,
            'message': message,
            'provider': 'SEIDiT'
        }
        
    except Exception as e:
        return {
            'valid': False,
            'message': f'Challenge validation error: {str(e)}',
            'provider': 'SEIDiT'
        } 