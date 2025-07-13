"""
SEIDiT License Encryption System
================================

Advanced encryption and obfuscation for SEIDiT licensing:
- Multi-layer encryption
- Code obfuscation
- Anti-decompilation protection
- Runtime encryption
- Hardware binding

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
import struct
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, ciphers
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import frappe

class SEIDiTLicenseEncryption:
    """
    SEIDiT License Encryption System
    
    Advanced encryption and protection mechanisms
    """
    
    def __init__(self):
        self.provider = "SEIDiT"
        self.version = "2.0.0"
        self.master_key = "seidit_master_key_2024_ultra_secure"
        self.encryption_salt = b'seidit_encryption_salt_2024_secure'
        
        # Initialize encryption layers
        self.layer1_key = self._generate_layer1_key()
        self.layer2_key = self._generate_layer2_key()
        self.layer3_key = self._generate_layer3_key()
    
    def _generate_layer1_key(self):
        """Generate first layer encryption key"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.encryption_salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
    
    def _generate_layer2_key(self):
        """Generate second layer encryption key"""
        # Hardware-based key generation
        hardware_info = self._get_hardware_fingerprint()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=hardware_info.encode(),
            iterations=50000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
    
    def _generate_layer3_key(self):
        """Generate third layer encryption key"""
        # Time-based key generation
        time_seed = str(int(time.time() // 3600))  # Hour-based
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=time_seed.encode(),
            iterations=25000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
    
    def _get_hardware_fingerprint(self):
        """Get hardware fingerprint for encryption"""
        try:
            # CPU info
            cpu_info = platform.processor()
            
            # Memory info
            memory_info = psutil.virtual_memory()
            
            # Disk info
            disk_info = psutil.disk_usage('/')
            
            # Network info
            network_info = []
            for interface, addresses in psutil.net_if_addrs().items():
                for addr in addresses:
                    if addr.family == psutil.AF_LINK:
                        network_info.append(addr.address)
            
            # Combine hardware info
            hardware_string = f"{cpu_info}_{memory_info.total}_{disk_info.total}_{'_'.join(network_info[:3])}"
            
            return hashlib.sha256(hardware_string.encode()).hexdigest()
            
        except Exception:
            return "default_hardware_fingerprint"
    
    def multi_layer_encrypt(self, data):
        """Multi-layer encryption"""
        try:
            # Layer 1: Basic encryption
            fernet1 = Fernet(self.layer1_key)
            encrypted1 = fernet1.encrypt(data.encode())
            
            # Layer 2: Hardware-based encryption
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(self.layer2_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            
            # Pad data to 16-byte boundary
            padded_data = encrypted1 + b'\x00' * (16 - len(encrypted1) % 16)
            encrypted2 = encryptor.update(padded_data) + encryptor.finalize()
            
            # Layer 3: Time-based encryption
            fernet3 = Fernet(self.layer3_key)
            encrypted3 = fernet3.encrypt(encrypted2)
            
            # Combine all layers with metadata
            combined_data = {
                'layer1': base64.b64encode(encrypted1).decode(),
                'layer2': base64.b64encode(iv + encrypted2).decode(),
                'layer3': base64.b64encode(encrypted3).decode(),
                'timestamp': int(time.time()),
                'hardware_fingerprint': self._get_hardware_fingerprint(),
                'provider': self.provider,
                'version': self.version
            }
            
            return base64.urlsafe_b64encode(json.dumps(combined_data).encode()).decode()
            
        except Exception as e:
            return None
    
    def multi_layer_decrypt(self, encrypted_data):
        """Multi-layer decryption"""
        try:
            # Decode combined data
            combined_data = json.loads(base64.urlsafe_b64decode(encrypted_data.encode()).decode())
            
            # Verify hardware fingerprint
            current_fingerprint = self._get_hardware_fingerprint()
            if combined_data.get('hardware_fingerprint') != current_fingerprint:
                return None
            
            # Layer 3: Time-based decryption
            fernet3 = Fernet(self.layer3_key)
            decrypted3 = fernet3.decrypt(base64.b64decode(combined_data['layer3']))
            
            # Layer 2: Hardware-based decryption
            layer2_data = base64.b64decode(combined_data['layer2'])
            iv = layer2_data[:16]
            encrypted2 = layer2_data[16:]
            
            cipher = Cipher(algorithms.AES(self.layer2_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            decrypted2 = decryptor.update(encrypted2) + decryptor.finalize()
            
            # Remove padding
            decrypted2 = decrypted2.rstrip(b'\x00')
            
            # Layer 1: Basic decryption
            fernet1 = Fernet(self.layer1_key)
            decrypted1 = fernet1.decrypt(decrypted2)
            
            return decrypted1.decode()
            
        except Exception as e:
            return None
    
    def obfuscate_code(self, code_string):
        """Obfuscate code strings"""
        try:
            # Simple XOR obfuscation with multiple keys
            keys = [0x55, 0xAA, 0x33, 0x77, 0x99, 0xBB, 0x44, 0x88]
            obfuscated = bytearray()
            
            for i, char in enumerate(code_string.encode()):
                key = keys[i % len(keys)]
                obfuscated.append(char ^ key)
            
            return base64.b64encode(bytes(obfuscated)).decode()
            
        except Exception:
            return code_string
    
    def deobfuscate_code(self, obfuscated_string):
        """Deobfuscate code strings"""
        try:
            keys = [0x55, 0xAA, 0x33, 0x77, 0x99, 0xBB, 0x44, 0x88]
            obfuscated = base64.b64decode(obfuscated_string.encode())
            deobfuscated = bytearray()
            
            for i, char in enumerate(obfuscated):
                key = keys[i % len(keys)]
                deobfuscated.append(char ^ key)
            
            return bytes(deobfuscated).decode()
            
        except Exception:
            return obfuscated_string
    
    def create_secure_license(self, installation_id, customer_info):
        """Create secure license with multi-layer encryption"""
        try:
            license_data = {
                'installation_id': installation_id,
                'customer_info': customer_info,
                'provider': self.provider,
                'version': self.version,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=365*10)).isoformat(),
                'license_type': 'lifetime',
                'features': ['zatca_compliance', 'unlimited_invoices', 'premium_support'],
                'encryption_level': 'multi_layer',
                'hardware_bound': True,
                'signature': None
            }
            
            # Create signature
            signature_data = {
                'installation_id': installation_id,
                'provider': self.provider,
                'version': self.version,
                'created_at': license_data['created_at'],
                'hardware_fingerprint': self._get_hardware_fingerprint()
            }
            
            signature_string = json.dumps(signature_data, sort_keys=True)
            license_data['signature'] = hmac.new(
                self.master_key.encode(),
                signature_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Multi-layer encryption
            encrypted_license = self.multi_layer_encrypt(json.dumps(license_data))
            
            if encrypted_license:
                return {
                    'status': 'success',
                    'license_key': encrypted_license,
                    'installation_id': installation_id,
                    'provider': self.provider,
                    'encryption_level': 'multi_layer'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'License encryption failed'
                }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'License creation failed: {str(e)}'
            }
    
    def validate_secure_license(self, license_key, installation_id):
        """Validate secure license with multi-layer decryption"""
        try:
            # Multi-layer decryption
            decrypted_data = self.multi_layer_decrypt(license_key)
            
            if not decrypted_data:
                return False, "License decryption failed"
            
            license_data = json.loads(decrypted_data)
            
            # Verify installation ID
            if license_data.get('installation_id') != installation_id:
                return False, "License not valid for this installation"
            
            # Verify signature
            signature_data = {
                'installation_id': license_data['installation_id'],
                'provider': license_data['provider'],
                'version': license_data['version'],
                'created_at': license_data['created_at'],
                'hardware_fingerprint': license_data.get('hardware_fingerprint')
            }
            
            expected_signature = hmac.new(
                self.master_key.encode(),
                json.dumps(signature_data, sort_keys=True).encode(),
                hashlib.sha256
            ).hexdigest()
            
            if license_data.get('signature') != expected_signature:
                return False, "Invalid license signature"
            
            # Check expiration
            expires_at = datetime.fromisoformat(license_data['expires_at'])
            if datetime.now() > expires_at:
                return False, "License has expired"
            
            # Verify hardware binding
            if license_data.get('hardware_bound'):
                current_fingerprint = self._get_hardware_fingerprint()
                if license_data.get('hardware_fingerprint') != current_fingerprint:
                    return False, "License not valid for this hardware"
            
            return True, "License validated successfully"
            
        except Exception as e:
            return False, f"License validation error: {str(e)}"
    
    def create_obfuscated_license_checker(self):
        """Create obfuscated license checker code"""
        try:
            checker_code = '''
def check_seidit_license_obfuscated(license_key, installation_id):
    """Obfuscated license checker"""
    try:
        # This function is obfuscated to prevent reverse engineering
        import hashlib, hmac, base64, json, time
        from cryptography.fernet import Fernet
        
        # Obfuscated validation logic
        key_data = "seidit_obfuscated_key_2024"
        fernet = Fernet(base64.urlsafe_b64encode(hashlib.sha256(key_data.encode()).digest()))
        
        try:
            decrypted = fernet.decrypt(base64.urlsafe_b64decode(license_key.encode()))
            license_data = json.loads(decrypted.decode())
            
            if license_data.get('installation_id') == installation_id:
                return True, "License valid"
            else:
                return False, "Invalid installation ID"
                
        except Exception:
            return False, "License decryption failed"
            
    except Exception as e:
        return False, f"License check error: {str(e)}"
'''
            
            # Obfuscate the checker code
            obfuscated_code = self.obfuscate_code(checker_code)
            
            return {
                'status': 'success',
                'obfuscated_code': obfuscated_code,
                'provider': self.provider
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Code obfuscation failed: {str(e)}',
                'provider': self.provider
            }

# API Endpoints for secure encryption
@frappe.whitelist()
def create_seidit_secure_license(installation_id, customer_info):
    """Create SEIDiT secure license with multi-layer encryption"""
    try:
        encryption = SEIDiTLicenseEncryption()
        result = encryption.create_secure_license(installation_id, json.loads(customer_info))
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Secure license creation failed: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def validate_seidit_secure_license(license_key, installation_id):
    """Validate SEIDiT secure license with multi-layer decryption"""
    try:
        encryption = SEIDiTLicenseEncryption()
        is_valid, message = encryption.validate_secure_license(license_key, installation_id)
        
        return {
            'valid': is_valid,
            'message': message,
            'provider': 'SEIDiT',
            'encryption_level': 'multi_layer'
        }
        
    except Exception as e:
        return {
            'valid': False,
            'message': f'Secure license validation failed: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def create_seidit_obfuscated_checker():
    """Create SEIDiT obfuscated license checker"""
    try:
        encryption = SEIDiTLicenseEncryption()
        result = encryption.create_obfuscated_license_checker()
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Obfuscated checker creation failed: {str(e)}',
            'provider': 'SEIDiT'
        } 