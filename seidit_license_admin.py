"""
SEIDiT License Administration System
===================================

Complete license administration system for SEIDiT to manage:
- License generation and management
- Customer database
- Usage monitoring
- License revocation
- Analytics and reporting

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.
"""

import hashlib
import hmac
import base64
import json
import time
import uuid
import sqlite3
import requests
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import frappe

class SEIDiTLicenseAdmin:
    """
    SEIDiT License Administration System
    
    Complete license management for SEIDiT administrators
    """
    
    def __init__(self):
        self.server_url = "https://license.seidit.com/api/v1"
        self.admin_key = "seidit_admin_key_2024_secure"
        self.provider = "SEIDiT"
        self.version = "2.0.0"
        
        # Initialize database
        self.init_database()
    
    def init_database(self):
        """Initialize administration database"""
        try:
            conn = sqlite3.connect('seidit_admin.db')
            cursor = conn.cursor()
            
            # Create customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id TEXT UNIQUE NOT NULL,
                    company_name TEXT NOT NULL,
                    contact_person TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    country TEXT,
                    created_at TEXT NOT NULL,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            # Create licenses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS licenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT UNIQUE NOT NULL,
                    customer_id TEXT NOT NULL,
                    installation_id TEXT NOT NULL,
                    license_type TEXT NOT NULL,
                    features TEXT,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    last_validated TEXT,
                    validation_count INTEGER DEFAULT 0,
                    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
                )
            ''')
            
            # Create usage analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT NOT NULL,
                    customer_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    invoice_count INTEGER DEFAULT 0,
                    FOREIGN KEY (license_key) REFERENCES licenses (license_key)
                )
            ''')
            
            # Create revenue tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS revenue_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id TEXT NOT NULL,
                    license_key TEXT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    payment_date TEXT NOT NULL,
                    payment_method TEXT,
                    invoice_number TEXT,
                    status TEXT DEFAULT 'paid',
                    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
                    FOREIGN KEY (license_key) REFERENCES licenses (license_key)
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Admin database initialization error: {str(e)}")
    
    def create_customer(self, customer_data):
        """Create new customer"""
        try:
            customer_id = f"SEIDiT_{uuid.uuid4().hex[:8].upper()}"
            
            conn = sqlite3.connect('seidit_admin.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO customers (
                    customer_id, company_name, contact_person, email, phone, 
                    address, country, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer_id,
                customer_data.get('company_name'),
                customer_data.get('contact_person'),
                customer_data.get('email'),
                customer_data.get('phone'),
                customer_data.get('address'),
                customer_data.get('country'),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'customer_id': customer_id,
                'message': 'Customer created successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Customer creation failed: {str(e)}'
            }
    
    def generate_license_for_customer(self, customer_id, installation_id, license_type='lifetime'):
        """Generate license for specific customer"""
        try:
            # Get customer info
            conn = sqlite3.connect('seidit_admin.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,))
            customer = cursor.fetchone()
            
            if not customer:
                return {
                    'status': 'error',
                    'message': 'Customer not found'
                }
            
            # Generate license
            license_data = {
                'customer_id': customer_id,
                'installation_id': installation_id,
                'license_type': license_type,
                'provider': self.provider,
                'version': self.version,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=365*10)).isoformat(),
                'features': ['zatca_compliance', 'unlimited_invoices', 'premium_support'],
                'signature': None
            }
            
            # Create signature
            signature_data = {
                'customer_id': customer_id,
                'installation_id': installation_id,
                'provider': self.provider,
                'version': self.version,
                'created_at': license_data['created_at']
            }
            
            signature_string = json.dumps(signature_data, sort_keys=True)
            license_data['signature'] = hmac.new(
                self.admin_key.encode(),
                signature_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Encrypt license data
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(json.dumps(license_data).encode())
            license_key = base64.urlsafe_b64encode(encrypted_data).decode()
            
            # Store in database
            cursor.execute('''
                INSERT INTO licenses (
                    license_key, customer_id, installation_id, license_type,
                    features, created_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                license_key, customer_id, installation_id, license_type,
                json.dumps(license_data['features']),
                license_data['created_at'], license_data['expires_at']
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'license_key': license_key,
                'customer_id': customer_id,
                'installation_id': installation_id,
                'license_type': license_type,
                'message': 'License generated successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'License generation failed: {str(e)}'
            }
    
    def get_customer_licenses(self, customer_id):
        """Get all licenses for a customer"""
        try:
            conn = sqlite3.connect('seidit_admin.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT l.*, c.company_name 
                FROM licenses l 
                JOIN customers c ON l.customer_id = c.customer_id 
                WHERE l.customer_id = ?
            ''', (customer_id,))
            
            licenses = cursor.fetchall()
            conn.close()
            
            return {
                'status': 'success',
                'licenses': licenses,
                'customer_id': customer_id
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get licenses: {str(e)}'
            }
    
    def revoke_license(self, license_key, reason="Admin revocation"):
        """Revoke license"""
        try:
            conn = sqlite3.connect('seidit_admin.db')
            cursor = conn.cursor()
            
            # Update license status
            cursor.execute('''
                UPDATE licenses SET is_active = 0 
                WHERE license_key = ?
            ''', (license_key,))
            
            # Log revocation
            cursor.execute('''
                INSERT INTO usage_analytics (license_key, customer_id, action, timestamp)
                SELECT license_key, customer_id, ?, ? FROM licenses WHERE license_key = ?
            ''', (f'revoked: {reason}', datetime.now().isoformat(), license_key))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'message': 'License revoked successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'License revocation failed: {str(e)}'
            }
    
    def get_usage_analytics(self, customer_id=None, days=30):
        """Get usage analytics"""
        try:
            conn = sqlite3.connect('seidit_admin.db')
            cursor = conn.cursor()
            
            if customer_id:
                cursor.execute('''
                    SELECT ua.*, c.company_name, l.license_type
                    FROM usage_analytics ua
                    JOIN licenses l ON ua.license_key = l.license_key
                    JOIN customers c ON l.customer_id = c.customer_id
                    WHERE l.customer_id = ? AND ua.timestamp >= ?
                    ORDER BY ua.timestamp DESC
                ''', (customer_id, (datetime.now() - timedelta(days=days)).isoformat()))
            else:
                cursor.execute('''
                    SELECT ua.*, c.company_name, l.license_type
                    FROM usage_analytics ua
                    JOIN licenses l ON ua.license_key = l.license_key
                    JOIN customers c ON l.customer_id = c.customer_id
                    WHERE ua.timestamp >= ?
                    ORDER BY ua.timestamp DESC
                ''', ((datetime.now() - timedelta(days=days)).isoformat(),))
            
            analytics = cursor.fetchall()
            conn.close()
            
            return {
                'status': 'success',
                'analytics': analytics,
                'period_days': days
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get analytics: {str(e)}'
            }
    
    def get_revenue_report(self, start_date=None, end_date=None):
        """Get revenue report"""
        try:
            conn = sqlite3.connect('seidit_admin.db')
            cursor = conn.cursor()
            
            if start_date and end_date:
                cursor.execute('''
                    SELECT rt.*, c.company_name, l.license_type
                    FROM revenue_tracking rt
                    JOIN customers c ON rt.customer_id = c.customer_id
                    JOIN licenses l ON rt.license_key = l.license_key
                    WHERE rt.payment_date BETWEEN ? AND ?
                    ORDER BY rt.payment_date DESC
                ''', (start_date, end_date))
            else:
                cursor.execute('''
                    SELECT rt.*, c.company_name, l.license_type
                    FROM revenue_tracking rt
                    JOIN customers c ON rt.customer_id = c.customer_id
                    JOIN licenses l ON rt.license_key = l.license_key
                    ORDER BY rt.payment_date DESC
                ''')
            
            revenue_data = cursor.fetchall()
            
            # Calculate totals
            total_revenue = sum(row[3] for row in revenue_data)  # amount column
            
            conn.close()
            
            return {
                'status': 'success',
                'revenue_data': revenue_data,
                'total_revenue': total_revenue,
                'period': f"{start_date} to {end_date}" if start_date and end_date else "All time"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get revenue report: {str(e)}'
            }
    
    def add_revenue_entry(self, customer_id, license_key, amount, currency='USD', payment_method='bank_transfer'):
        """Add revenue entry"""
        try:
            invoice_number = f"SEIDiT_INV_{uuid.uuid4().hex[:8].upper()}"
            
            conn = sqlite3.connect('seidit_admin.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO revenue_tracking (
                    customer_id, license_key, amount, currency, payment_date,
                    payment_method, invoice_number, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer_id, license_key, amount, currency,
                datetime.now().isoformat(), payment_method, invoice_number, 'paid'
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'invoice_number': invoice_number,
                'message': 'Revenue entry added successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to add revenue entry: {str(e)}'
            }

# API Endpoints for license administration
@frappe.whitelist()
def create_seidit_customer(customer_data):
    """Create SEIDiT customer (admin only)"""
    try:
        if not frappe.has_permission("System Manager"):
            return {
                'status': 'error',
                'message': 'Unauthorized access',
                'provider': 'SEIDiT'
            }
        
        admin = SEIDiTLicenseAdmin()
        result = admin.create_customer(json.loads(customer_data))
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Customer creation error: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def generate_seidit_customer_license(customer_id, installation_id, license_type='lifetime'):
    """Generate SEIDiT license for customer (admin only)"""
    try:
        if not frappe.has_permission("System Manager"):
            return {
                'status': 'error',
                'message': 'Unauthorized access',
                'provider': 'SEIDiT'
            }
        
        admin = SEIDiTLicenseAdmin()
        result = admin.generate_license_for_customer(customer_id, installation_id, license_type)
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'License generation error: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def get_seidit_customer_licenses(customer_id):
    """Get SEIDiT customer licenses (admin only)"""
    try:
        if not frappe.has_permission("System Manager"):
            return {
                'status': 'error',
                'message': 'Unauthorized access',
                'provider': 'SEIDiT'
            }
        
        admin = SEIDiTLicenseAdmin()
        result = admin.get_customer_licenses(customer_id)
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to get licenses: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def revoke_seidit_license(license_key, reason="Admin revocation"):
    """Revoke SEIDiT license (admin only)"""
    try:
        if not frappe.has_permission("System Manager"):
            return {
                'status': 'error',
                'message': 'Unauthorized access',
                'provider': 'SEIDiT'
            }
        
        admin = SEIDiTLicenseAdmin()
        result = admin.revoke_license(license_key, reason)
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'License revocation error: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def get_seidit_usage_analytics(customer_id=None, days=30):
    """Get SEIDiT usage analytics (admin only)"""
    try:
        if not frappe.has_permission("System Manager"):
            return {
                'status': 'error',
                'message': 'Unauthorized access',
                'provider': 'SEIDiT'
            }
        
        admin = SEIDiTLicenseAdmin()
        result = admin.get_usage_analytics(customer_id, int(days))
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Analytics error: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def get_seidit_revenue_report(start_date=None, end_date=None):
    """Get SEIDiT revenue report (admin only)"""
    try:
        if not frappe.has_permission("System Manager"):
            return {
                'status': 'error',
                'message': 'Unauthorized access',
                'provider': 'SEIDiT'
            }
        
        admin = SEIDiTLicenseAdmin()
        result = admin.get_revenue_report(start_date, end_date)
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Revenue report error: {str(e)}',
            'provider': 'SEIDiT'
        } 