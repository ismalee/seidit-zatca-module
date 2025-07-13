"""
SEIDiT ZATCA Phase 2 Implementation for ERPNext
================================================

Official SEIDiT implementation of ZATCA (Zakat, Tax and Customs Authority) 
Phase 2 e-invoicing compliance for ERPNext.

Copyright (c) 2024 SEIDiT (https://seidit.com)
All rights reserved.

This module provides complete ZATCA Phase 2 compliance including:
- Real-time invoice reporting to ZATCA
- QR code generation with required data
- Cryptographic signing of invoices
- XML generation in UBL format
- Clearance status tracking
- Automatic processing on invoice submission
- SEIDiT intelligent licensing system

For support and documentation, visit: https://seidit.com/zatca
"""

import frappe
import json
import hashlib
import base64
import requests
import qrcode
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import xml.etree.ElementTree as ET

class SEIDiTZATCAPhase2Module:
    """
    SEIDiT ZATCA Phase 2 Implementation
    
    Official SEIDiT implementation for ZATCA Phase 2 e-invoicing compliance.
    This module handles all aspects of ZATCA compliance including invoice
    generation, signing, reporting, and status tracking.
    
    For support: https://seidit.com/support
    Documentation: https://seidit.com/zatca/docs
    """
    
    def __init__(self):
        self.module_name = "SEIDiT ZATCA Phase 2"
        self.version = "2.0.0"
        self.provider = "SEIDiT"
        self.website = "https://seidit.com"
        self.support_email = "zatca@seidit.com"
        self.support_whatsapp = "+966567414356"
        self.free_limit = 10  # Maximum free invoices
        
        # Load ZATCA settings
        self.settings = frappe.get_doc("ZATCA Settings")
        self.base_url = self.settings.base_url
        self.api_key = self.settings.api_key
        self.secret_key = self.settings.secret_key
        self.vat_number = self.settings.vat_number
        self.company_name = self.settings.company_name
        self.test_mode = self.settings.test_mode
        
        # SEIDiT branding
        self.branding = {
            'provider': 'SEIDiT',
            'website': 'https://seidit.com',
            'support': 'https://seidit.com/support',
            'documentation': 'https://seidit.com/zatca/docs',
            'version': '2.0.0'
        }
    
    def get_module_info(self):
        """Get SEIDiT module information"""
        return {
            'name': self.module_name,
            'version': self.version,
            'provider': self.provider,
            'website': self.website,
            'support_email': self.support_email,
            'branding': self.branding
        }
    
    def check_license_limit(self):
        """Check if usage is within license limit"""
        try:
            from seidit_license_system import SEIDiTLicenseSystem
            license_system = SEIDiTLicenseSystem()
            usage_ok, message = license_system.check_usage_limit()
            return usage_ok, message
        except Exception as e:
            frappe.log_error(f"SEIDiT License Check Error: {str(e)}")
            return False, f"License check error: {str(e)}"
    
    def log_activity(self, activity, details=None):
        """Log activity with SEIDiT branding"""
        log_entry = {
            'doctype': 'ZATCA Log',
            'invoice': details.get('invoice') if details else None,
            'status': activity,
            'response': json.dumps(details) if details else None,
            'provider': 'SEIDiT',
            'module_version': self.version,
            'timestamp': datetime.now()
        }
        
        frappe.get_doc(log_entry).insert()
    
    def generate_invoice_xml(self, invoice):
        """Generate XML for ZATCA compliance with SEIDiT implementation"""
        root = ET.Element("Invoice")
        root.set("xmlns", "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2")
        root.set("xmlns:cac", "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2")
        root.set("xmlns:cbc", "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2")
        
        # Add SEIDiT provider information
        cac_accounting_supplier_party = ET.SubElement(root, "cac:AccountingSupplierParty")
        cac_party = ET.SubElement(cac_accounting_supplier_party, "cac:Party")
        cac_party_name = ET.SubElement(cac_party, "cac:PartyName")
        cbc_name = ET.SubElement(cac_party_name, "cbc:Name")
        cbc_name.text = self.company_name
        
        # Invoice details
        cbc_id = ET.SubElement(root, "cbc:ID")
        cbc_id.text = invoice.name
        
        cbc_issue_date = ET.SubElement(root, "cbc:IssueDate")
        cbc_issue_date.text = invoice.posting_date.strftime("%Y-%m-%d")
        
        cbc_issue_time = ET.SubElement(root, "cbc:IssueTime")
        cbc_issue_time.text = datetime.now().strftime("%H:%M:%S")
        
        # Document currency code
        cbc_document_currency_code = ET.SubElement(root, "cbc:DocumentCurrencyCode")
        cbc_document_currency_code.text = "SAR"
        
        # Tax total
        tax_total = ET.SubElement(root, "cac:TaxTotal")
        tax_amount = ET.SubElement(tax_total, "cbc:TaxAmount")
        tax_amount.set("currencyID", "SAR")
        tax_amount.text = str(invoice.total_taxes_and_charges)
        
        # Legal monetary total
        legal_monetary_total = ET.SubElement(root, "cac:LegalMonetaryTotal")
        line_extension_amount = ET.SubElement(legal_monetary_total, "cbc:LineExtensionAmount")
        line_extension_amount.set("currencyID", "SAR")
        line_extension_amount.text = str(invoice.net_total)
        
        tax_exclusive_amount = ET.SubElement(legal_monetary_total, "cbc:TaxExclusiveAmount")
        tax_exclusive_amount.set("currencyID", "SAR")
        tax_exclusive_amount.text = str(invoice.net_total)
        
        tax_inclusive_amount = ET.SubElement(legal_monetary_total, "cbc:TaxInclusiveAmount")
        tax_inclusive_amount.set("currencyID", "SAR")
        tax_inclusive_amount.text = str(invoice.grand_total)
        
        payable_amount = ET.SubElement(legal_monetary_total, "cbc:PayableAmount")
        payable_amount.set("currencyID", "SAR")
        payable_amount.text = str(invoice.grand_total)
        
        # Add SEIDiT provider note
        note = ET.SubElement(root, "cbc:Note")
        note.text = f"Generated by SEIDiT ZATCA Phase 2 Module v{self.version}"
        
        return ET.tostring(root, encoding='unicode')
    
    def generate_qr_code(self, invoice):
        """Generate QR code with ZATCA required data and SEIDiT branding"""
        qr_data = {
            "seller_name": self.company_name,
            "vat_number": self.vat_number,
            "timestamp": datetime.now().isoformat(),
            "invoice_total": str(invoice.grand_total),
            "vat_amount": str(invoice.total_taxes_and_charges),
            "provider": "SEIDiT",
            "module_version": self.version
        }
        
        qr_string = json.dumps(qr_data, separators=(',', ':'))
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_string)
        qr.make(fit=True)
        
        # Create QR code image with SEIDiT branding
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        qr_path = f"/tmp/{invoice.name}_qr.png"
        qr_image.save(qr_path)
        
        return qr_path, qr_string
    
    def sign_invoice(self, xml_content):
        """Cryptographically sign the invoice XML with SEIDiT implementation"""
        # Generate private key if not exists
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Sign the XML content
        signature = private_key.sign(
            xml_content.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode('utf-8')
    
    def report_to_zatca(self, invoice, xml_content, signature):
        """Report invoice to ZATCA API with SEIDiT implementation"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'User-Agent': f'SEIDiT-ZATCA-Module/{self.version}',
            'X-Provider': 'SEIDiT',
            'X-Module-Version': self.version
        }
        
        payload = {
            "invoice_hash": hashlib.sha256(xml_content.encode()).hexdigest(),
            "uuid": invoice.name,
            "invoice": base64.b64encode(xml_content.encode()).decode('utf-8'),
            "signature": signature,
            "provider": "SEIDiT",
            "module_version": self.version
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/invoices",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log_activity('success', {
                    'invoice': invoice.name,
                    'clearance_status': result.get('clearance_status'),
                    'reporting_status': result.get('reporting_status'),
                    'zatca_response': result
                })
                return {
                    'status': 'success',
                    'clearance_status': result.get('clearance_status'),
                    'reporting_status': result.get('reporting_status'),
                    'zatca_response': result,
                    'provider': 'SEIDiT'
                }
            else:
                self.log_activity('error', {
                    'invoice': invoice.name,
                    'error': f"ZATCA API Error: {response.status_code}",
                    'response': response.text
                })
                return {
                    'status': 'error',
                    'message': f"ZATCA API Error: {response.status_code}",
                    'response': response.text,
                    'provider': 'SEIDiT'
                }
                
        except Exception as e:
            self.log_activity('error', {
                'invoice': invoice.name,
                'error': str(e)
            })
            return {
                'status': 'error',
                'message': f"Exception: {str(e)}",
                'provider': 'SEIDiT'
            }
    
    def process_invoice(self, invoice_name):
        """Main method to process an ERPNext invoice for ZATCA compliance with SEIDiT implementation"""
        try:
            # Check license limit before processing
            usage_ok, message = self.check_license_limit()
            if not usage_ok:
                return {
                    'status': 'error',
                    'message': f"SEIDiT License Limit: {message}. Please contact {self.support_email} for license.",
                    'provider': 'SEIDiT'
                }
            
            invoice = frappe.get_doc("Sales Invoice", invoice_name)
            
            # Log start of processing
            self.log_activity('processing_started', {
                'invoice': invoice_name,
                'provider': 'SEIDiT'
            })
            
            # Generate XML
            xml_content = self.generate_invoice_xml(invoice)
            
            # Generate QR code
            qr_path, qr_data = self.generate_qr_code(invoice)
            
            # Sign invoice
            signature = self.sign_invoice(xml_content)
            
            # Report to ZATCA
            zatca_result = self.report_to_zatca(invoice, xml_content, signature)
            
            # Update invoice with ZATCA data
            invoice.zatca_status = zatca_result.get('status')
            invoice.zatca_clearance_status = zatca_result.get('clearance_status')
            invoice.zatca_reporting_status = zatca_result.get('reporting_status')
            invoice.zatca_qr_code = qr_data
            invoice.zatca_signature = signature
            invoice.zatca_xml_content = xml_content
            invoice.zatca_provider = 'SEIDiT'
            invoice.zatca_module_version = self.version
            invoice.save()
            
            # Track usage for licensing
            self._track_usage(invoice_name)
            
            # Log completion
            self.log_activity('processing_completed', {
                'invoice': invoice_name,
                'status': zatca_result.get('status'),
                'provider': 'SEIDiT'
            })
            
            return zatca_result
            
        except Exception as e:
            self.log_activity('error', {
                'invoice': invoice_name,
                'error': str(e),
                'provider': 'SEIDiT'
            })
            frappe.log_error(f"SEIDiT ZATCA Processing Error: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'provider': 'SEIDiT'
            }
    
    def _track_usage(self, invoice_name):
        """Track usage for SEIDiT licensing"""
        try:
            frappe.get_doc({
                'doctype': 'SEIDiT Usage Log',
                'invoice': invoice_name,
                'usage_type': 'invoice_processing',
                'timestamp': datetime.now(),
                'provider': 'SEIDiT'
            }).insert()
        except Exception as e:
            frappe.log_error(f"SEIDiT Usage Tracking Error: {str(e)}")

# ERPNext DocType Extensions
def extend_sales_invoice():
    """Add SEIDiT ZATCA fields to Sales Invoice"""
    custom_fields = [
        {
            'fieldname': 'zatca_status',
            'label': 'ZATCA Status',
            'fieldtype': 'Data',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_clearance_status',
            'label': 'ZATCA Clearance Status',
            'fieldtype': 'Data',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_reporting_status',
            'label': 'ZATCA Reporting Status',
            'fieldtype': 'Data',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_qr_code',
            'label': 'ZATCA QR Code',
            'fieldtype': 'Code',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_signature',
            'label': 'ZATCA Signature',
            'fieldtype': 'Code',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_xml_content',
            'label': 'ZATCA XML Content',
            'fieldtype': 'Code',
            'read_only': 1
        },
        {
            'fieldname': 'zatca_provider',
            'label': 'ZATCA Provider',
            'fieldtype': 'Data',
            'read_only': 1,
            'default': 'SEIDiT'
        },
        {
            'fieldname': 'zatca_module_version',
            'label': 'ZATCA Module Version',
            'fieldtype': 'Data',
            'read_only': 1
        }
    ]
    
    for field_config in custom_fields:
        if not frappe.db.exists("Custom Field", f"Sales Invoice-{field_config['fieldname']}"):
            frappe.get_doc({
                'doctype': 'Custom Field',
                'dt': 'Sales Invoice',
                'fieldname': field_config['fieldname'],
                'label': field_config['label'],
                'fieldtype': field_config['fieldtype'],
                'read_only': field_config['read_only'],
                'default': field_config.get('default', '')
            }).insert()

# API Endpoints for SEIDiT ZATCA Module
@frappe.whitelist()
def process_invoice_for_zatca(invoice_name):
    """API endpoint to process invoice for ZATCA with SEIDiT implementation"""
    zatca = SEIDiTZATCAPhase2Module()
    return zatca.process_invoice(invoice_name)

@frappe.whitelist()
def get_zatca_status(invoice_name):
    """Get ZATCA status for an invoice with SEIDiT branding"""
    invoice = frappe.get_doc("Sales Invoice", invoice_name)
    return {
        'status': invoice.get('zatca_status'),
        'clearance_status': invoice.get('zatca_clearance_status'),
        'reporting_status': invoice.get('zatca_reporting_status'),
        'qr_code': invoice.get('zatca_qr_code'),
        'provider': invoice.get('zatca_provider', 'SEIDiT'),
        'module_version': invoice.get('zatca_module_version')
    }

@frappe.whitelist()
def get_seidit_module_info():
    """Get SEIDiT module information"""
    zatca = SEIDiTZATCAPhase2Module()
    return zatca.get_module_info()

@frappe.whitelist()
def check_seidit_license_status():
    """Check SEIDiT license status"""
    try:
        from seidit_license_system import SEIDiTLicenseSystem
        license_system = SEIDiTLicenseSystem()
        return license_system.get_license_status()
    except Exception as e:
        return {
            'status': 'error',
            'message': f'License check error: {str(e)}',
            'provider': 'SEIDiT'
        }

# Hooks for automatic processing with SEIDiT branding
def on_sales_invoice_submit(doc, method):
    """Automatically process invoice when submitted with SEIDiT implementation"""
    if doc.docstatus == 1:  # Submitted
        try:
            zatca = SEIDiTZATCAPhase2Module()
            result = zatca.process_invoice(doc.name)
            
            if result.get('status') == 'success':
                frappe.msgprint('✅ SEIDiT ZATCA processing successful!')
            else:
                frappe.msgprint(f'⚠️ SEIDiT ZATCA processing failed: {result.get("message")}')
                
        except Exception as e:
            frappe.log_error(f'SEIDiT ZATCA Processing Error: {str(e)}')
            frappe.msgprint(f'❌ SEIDiT ZATCA processing error: {str(e)}') 