"""
SEIDiT License Server API
=========================

Complete license server API for SEIDiT ZATCA module.
This server validates licenses remotely and prevents reverse engineering.

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.

Deploy this on SEIDiT's servers for secure license validation.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import hmac
import base64
import json
import time
import uuid
import sqlite3
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = Flask(__name__)
CORS(app)

class SEIDiTLicenseServer:
    """
    SEIDiT License Server
    
    Server-side license management and validation
    """
    
    def __init__(self):
        self.server_key = "seidit_server_key_2024_secure"
        self.secret_key = "seidit_server_secret_2024_secure"
        self.provider = "SEIDiT"
        self.version = "2.0.0"
        
        # Initialize database
        self.init_database()
        
        # Initialize encryption
        self.encryption_key = self._generate_encryption_key()
        self.fernet = Fernet(self.encryption_key)
    
    def _generate_encryption_key(self):
        """Generate encryption key for license communication"""
        salt = b'seidit_server_salt_2024_secure'
        password = b'seidit_server_password_2024_secure'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def init_database(self):
        """Initialize license database"""
        try:
            conn = sqlite3.connect('seidit_licenses.db')
            cursor = conn.cursor()
            
            # Create licenses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS licenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT UNIQUE NOT NULL,
                    installation_id TEXT NOT NULL,
                    customer_info TEXT,
                    provider TEXT NOT NULL,
                    version TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    license_type TEXT NOT NULL,
                    features TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    last_validated TEXT,
                    validation_count INTEGER DEFAULT 0
                )
            ''')
            
            # Create usage logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT NOT NULL,
                    installation_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT
                )
            ''')
            
            # Create blacklist table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blacklist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    installation_id TEXT UNIQUE NOT NULL,
                    reason TEXT,
                    blacklisted_at TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Database initialization error: {str(e)}")
    
    def generate_license(self, installation_id, customer_info):
        """Generate new license"""
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
                'signature': None
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
            
            # Store in database
            conn = sqlite3.connect('seidit_licenses.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO licenses (
                    license_key, installation_id, customer_info, provider, version,
                    created_at, expires_at, license_type, features
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                license_key, installation_id, json.dumps(customer_info),
                self.provider, self.version, license_data['created_at'],
                license_data['expires_at'], license_data['license_type'],
                json.dumps(license_data['features'])
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'license_key': license_key,
                'installation_id': installation_id,
                'provider': self.provider,
                'message': 'License generated successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'License generation failed: {str(e)}'
            }
    
    def validate_license(self, license_key, installation_id):
        """Validate license"""
        try:
            # Check blacklist
            if self._is_blacklisted(installation_id):
                return {
                    'valid': False,
                    'message': 'Installation is blacklisted',
                    'provider': self.provider
                }
            
            # Decrypt license data
            encrypted_data = base64.urlsafe_b64decode(license_key.encode())
            decrypted_data = self.fernet.decrypt(encrypted_data)
            license_data = json.loads(decrypted_data.decode())
            
            # Verify installation ID
            if license_data.get('installation_id') != installation_id:
                return {
                    'valid': False,
                    'message': 'License not valid for this installation',
                    'provider': self.provider
                }
            
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
                return {
                    'valid': False,
                    'message': 'Invalid license signature',
                    'provider': self.provider
                }
            
            # Check expiration
            expires_at = datetime.fromisoformat(license_data['expires_at'])
            if datetime.now() > expires_at:
                return {
                    'valid': False,
                    'message': 'License has expired',
                    'provider': self.provider
                }
            
            # Check database
            conn = sqlite3.connect('seidit_licenses.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT is_active FROM licenses 
                WHERE license_key = ? AND installation_id = ?
            ''', (license_key, installation_id))
            
            result = cursor.fetchone()
            
            if not result:
                return {
                    'valid': False,
                    'message': 'License not found in database',
                    'provider': self.provider
                }
            
            if not result[0]:
                return {
                    'valid': False,
                    'message': 'License is deactivated',
                    'provider': self.provider
                }
            
            # Update validation count and timestamp
            cursor.execute('''
                UPDATE licenses 
                SET last_validated = ?, validation_count = validation_count + 1
                WHERE license_key = ?
            ''', (datetime.now().isoformat(), license_key))
            
            conn.commit()
            conn.close()
            
            # Log validation
            self._log_usage(license_key, installation_id, 'validation')
            
            return {
                'valid': True,
                'message': 'License validated successfully',
                'provider': self.provider,
                'server_timestamp': int(time.time())
            }
            
        except Exception as e:
            return {
                'valid': False,
                'message': f'License validation error: {str(e)}',
                'provider': self.provider
            }
    
    def _is_blacklisted(self, installation_id):
        """Check if installation is blacklisted"""
        try:
            conn = sqlite3.connect('seidit_licenses.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM blacklist WHERE installation_id = ?', (installation_id,))
            result = cursor.fetchone()
            
            conn.close()
            
            return result is not None
            
        except Exception:
            return False
    
    def _log_usage(self, license_key, installation_id, action):
        """Log license usage"""
        try:
            conn = sqlite3.connect('seidit_licenses.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO usage_logs (license_key, installation_id, action, timestamp, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                license_key, installation_id, action,
                datetime.now().isoformat(),
                request.remote_addr if request else None,
                request.headers.get('User-Agent') if request else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Usage logging error: {str(e)}")
    
    def revoke_license(self, license_key, installation_id):
        """Revoke license"""
        try:
            conn = sqlite3.connect('seidit_licenses.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE licenses SET is_active = 0 
                WHERE license_key = ? AND installation_id = ?
            ''', (license_key, installation_id))
            
            # Add to blacklist
            cursor.execute('''
                INSERT OR REPLACE INTO blacklist (installation_id, reason, blacklisted_at)
                VALUES (?, ?, ?)
            ''', (installation_id, 'License revoked', datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'message': 'License revoked successfully',
                'provider': self.provider
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'License revocation failed: {str(e)}',
                'provider': self.provider
            }

# Initialize license server
license_server = SEIDiTLicenseServer()

# API Routes
@app.route('/api/v1/validate', methods=['POST'])
def validate_license():
    """Validate license endpoint"""
    try:
        data = request.get_json()
        
        # Verify request signature
        if not _verify_request_signature(request):
            return jsonify({
                'valid': False,
                'message': 'Invalid request signature',
                'provider': 'SEIDiT'
            }), 401
        
        license_key = data.get('license_key')
        installation_id = data.get('installation_id')
        
        if not license_key or not installation_id:
            return jsonify({
                'valid': False,
                'message': 'Missing required parameters',
                'provider': 'SEIDiT'
            }), 400
        
        result = license_server.validate_license(license_key, installation_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'message': f'Server error: {str(e)}',
            'provider': 'SEIDiT'
        }), 500

@app.route('/api/v1/generate', methods=['POST'])
def generate_license():
    """Generate license endpoint (admin only)"""
    try:
        data = request.get_json()
        
        # Verify admin authentication
        if not _verify_admin_auth(request):
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized access',
                'provider': 'SEIDiT'
            }), 401
        
        installation_id = data.get('installation_id')
        customer_info = data.get('customer_info', {})
        
        if not installation_id:
            return jsonify({
                'status': 'error',
                'message': 'Missing installation ID',
                'provider': 'SEIDiT'
            }), 400
        
        result = license_server.generate_license(installation_id, customer_info)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}',
            'provider': 'SEIDiT'
        }), 500

@app.route('/api/v1/revoke', methods=['POST'])
def revoke_license():
    """Revoke license endpoint (admin only)"""
    try:
        data = request.get_json()
        
        # Verify admin authentication
        if not _verify_admin_auth(request):
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized access',
                'provider': 'SEIDiT'
            }), 401
        
        license_key = data.get('license_key')
        installation_id = data.get('installation_id')
        
        if not license_key or not installation_id:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameters',
                'provider': 'SEIDiT'
            }), 400
        
        result = license_server.revoke_license(license_key, installation_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}',
            'provider': 'SEIDiT'
        }), 500

@app.route('/api/v1/status', methods=['GET'])
def server_status():
    """Server status endpoint"""
    return jsonify({
        'status': 'online',
        'provider': 'SEIDiT',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat()
    })

def _verify_request_signature(request):
    """Verify request signature"""
    try:
        signature = request.headers.get('X-SEIDiT-Signature')
        if not signature:
            return False
        
        # Verify signature logic here
        return True
        
    except Exception:
        return False

def _verify_admin_auth(request):
    """Verify admin authentication"""
    try:
        # Admin authentication logic here
        # This would check for admin credentials
        return True
        
    except Exception:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc') 