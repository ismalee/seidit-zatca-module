import frappe
from frappe import _
from frappe.utils import now_datetime
import webbrowser
import json

class SEIDiTZATCASetupWizard:
    """
    SEIDiT ZATCA Phase 2 Setup Wizard
    
    Official SEIDiT implementation for easy ZATCA Phase 2 setup in ERPNext.
    This wizard guides users through the complete setup process with step-by-step
    instructions and automated testing.
    
    For support: https://seidit.com/support
    Documentation: https://seidit.com/zatca/docs
    """
    
    def __init__(self):
        self.provider = "SEIDiT"
        self.website = "https://seidit.com"
        self.support_email = "zatca@seidit.com"
        self.support_whatsapp = "+966567414356"
        self.documentation_url = "https://seidit.com/zatca/docs"
        self.version = "2.0.0"
        self.free_limit = 10  # Maximum free invoices
        
        self.steps = [
            "welcome",
            "vat_registration",
            "zatca_portal_access",
            "api_credentials",
            "test_connection",
            "live_activation",
            "invoice_testing",
            "license_warning",
            "completion"
        ]
    
    def get_wizard_data(self):
        """Get current wizard data"""
        return frappe.get_doc("ZATCA Setup Wizard", "Default") if frappe.db.exists("ZATCA Setup Wizard", "Default") else None
    
    def create_wizard(self):
        """Create setup wizard with SEIDiT branding"""
        if not frappe.db.exists("ZATCA Setup Wizard", "Default"):
            frappe.get_doc({
                'doctype': 'ZATCA Setup Wizard',
                'name': 'Default',
                'current_step': 'welcome',
                'vat_number': '',
                'company_name': '',
                'zatca_username': '',
                'zatca_password': '',
                'api_key': '',
                'secret_key': '',
                'test_mode': 1,
                'setup_complete': 0,
                'provider': 'SEIDiT',
                'module_version': self.version
            }).insert()
    
    def update_step(self, step, data=None):
        """Update wizard step"""
        wizard = self.get_wizard_data()
        if wizard:
            wizard.current_step = step
            if data:
                for key, value in data.items():
                    setattr(wizard, key, value)
            wizard.save()
    
    def get_step_content(self, step):
        """Get content for each step with SEIDiT branding"""
        content = {
            'welcome': {
                'title': 'Welcome to SEIDiT ZATCA Phase 2 Setup',
                'description': 'This wizard will guide you through setting up ZATCA Phase 2 e-invoicing compliance for your ERPNext system using SEIDiT\'s official implementation.',
                'instructions': [
                    '✅ Complete ZATCA Phase 2 compliance',
                    '✅ Automatic invoice processing',
                    '✅ QR code generation',
                    '✅ Digital signing',
                    '✅ Real-time reporting to ZATCA',
                    '✅ SEIDiT professional support'
                ],
                'estimated_time': '15-20 minutes',
                'requirements': [
                    'VAT registration number',
                    'ZATCA portal access',
                    'Company details'
                ],
                'provider_info': {
                    'name': 'SEIDiT',
                    'website': 'https://seidit.com',
                    'support': 'https://seidit.com/support',
                    'email': 'support@seidit.com'
                }
            },
            'vat_registration': {
                'title': 'VAT Registration Verification',
                'description': 'First, let\'s verify your VAT registration details for ZATCA compliance.',
                'fields': [
                    {
                        'fieldname': 'vat_number',
                        'label': 'VAT Registration Number',
                        'placeholder': 'e.g., 123456789012345',
                        'help': 'Enter your 15-digit VAT registration number'
                    },
                    {
                        'fieldname': 'company_name',
                        'label': 'Company Name',
                        'placeholder': 'Your Company Name',
                        'help': 'Enter your registered company name as it appears on VAT certificate'
                    }
                ]
            },
            'zatca_portal_access': {
                'title': 'ZATCA Portal Access',
                'description': 'Now we need to get your API credentials from the ZATCA portal. SEIDiT will guide you through this process.',
                'instructions': [
                    '1. Go to ZATCA E-Invoicing Portal',
                    '2. Login with your VAT credentials',
                    '3. Navigate to Developer Portal',
                    '4. Generate API credentials',
                    '5. Copy the credentials to the form below'
                ],
                'portal_links': {
                    'test': 'https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal/test',
                    'live': 'https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal'
                },
                'provider_note': 'SEIDiT provides professional support for ZATCA portal access and API credential generation.'
            },
            'api_credentials': {
                'title': 'API Credentials Setup',
                'description': 'Enter the API credentials you obtained from the ZATCA portal. SEIDiT ensures secure handling of your credentials.',
                'fields': [
                    {
                        'fieldname': 'api_key',
                        'label': 'API Key',
                        'placeholder': 'Your API Key from ZATCA',
                        'help': 'Copy the API key from ZATCA developer portal'
                    },
                    {
                        'fieldname': 'secret_key',
                        'label': 'Secret Key',
                        'placeholder': 'Your Secret Key from ZATCA',
                        'help': 'Copy the secret key from ZATCA developer portal'
                    },
                    {
                        'fieldname': 'test_mode',
                        'label': 'Test Mode',
                        'help': 'Enable test mode for initial testing (recommended)'
                    }
                ],
                'security_note': 'SEIDiT ensures all credentials are stored securely and encrypted.'
            },
            'test_connection': {
                'title': 'Test Connection',
                'description': 'Let\'s test your connection to ZATCA before going live. SEIDiT will verify everything is working correctly.',
                'test_steps': [
                    '1. Testing API connection...',
                    '2. Validating credentials...',
                    '3. Checking VAT number...',
                    '4. Testing invoice submission...'
                ],
                'provider_support': 'SEIDiT provides 24/7 support for connection issues and troubleshooting.'
            },
            'live_activation': {
                'title': 'Live Mode Activation',
                'description': 'Switch to live mode for production use. SEIDiT ensures a smooth transition to live operations.',
                'warning': '⚠️ Make sure you have thoroughly tested in test mode before switching to live mode.',
                'instructions': [
                    '1. Disable test mode',
                    '2. Update API credentials for live environment',
                    '3. Test with a real invoice',
                    '4. Monitor clearance status'
                ],
                'provider_guidance': 'SEIDiT provides professional guidance for live mode activation and monitoring.'
            },
            'invoice_testing': {
                'title': 'Invoice Testing',
                'description': 'Test the complete invoice processing workflow with SEIDiT\'s implementation.',
                'test_invoice': {
                    'customer': 'Test Customer',
                    'items': ['Test Item 1', 'Test Item 2'],
                    'amount': 100.00,
                    'vat': 15.00
                },
                'provider_features': 'SEIDiT implementation includes advanced testing features and comprehensive error handling.'
            },
            'license_warning': {
                'title': 'SEIDiT License Information',
                'description': 'Important information about SEIDiT licensing and usage limits.',
                'license_info': {
                    'free_limit': self.free_limit,
                    'license_required': 'After processing 10 invoices, a SEIDiT license is required for unlimited usage.',
                    'installation_id': self._get_installation_id(),
                    'support_email': self.support_email,
                    'support_whatsapp': self.support_whatsapp
                },
                'warning_message': f'⚠️ IMPORTANT: You can process up to {self.free_limit} invoices for free. After that, a SEIDiT license is required for unlimited usage.',
                'instructions': [
                    '1. Your installation ID has been generated',
                    '2. Share this ID with SEIDiT to get your license',
                    '3. License is tied to this specific installation',
                    '4. One-time use - cannot be reused on other installations',
                    '5. Lifetime validity - no expiration'
                ],
                'contact_info': {
                    'email': self.support_email,
                    'whatsapp': self.support_whatsapp,
                    'website': self.website
                }
            },
            'completion': {
                'title': 'Setup Complete!',
                'description': 'Congratulations! Your SEIDiT ZATCA Phase 2 setup is complete and ready for production use.',
                'next_steps': [
                    'Create your first invoice',
                    'Monitor ZATCA status',
                    'Check clearance reports',
                    'Set up monitoring alerts',
                    'Contact SEIDiT for license when needed'
                ],
                'provider_support': {
                    'website': 'https://seidit.com',
                    'support': 'https://seidit.com/support',
                    'email': 'support@seidit.com',
                    'documentation': 'https://seidit.com/zatca/docs'
                }
            }
        }
        return content.get(step, {})
    
    def _get_installation_id(self):
        """Get installation ID for license"""
        try:
            from seidit_license_system import SEIDiTLicenseSystem
            license_system = SEIDiTLicenseSystem()
            installation_info = license_system.get_installation_info()
            return installation_info.get('installation_id')
        except:
            return "INSTALLATION_ID_NOT_AVAILABLE"

class SEIDiTZATCAWizardPage:
    """ERPNext page for SEIDiT ZATCA setup wizard"""
    
    def __init__(self):
        self.wizard = SEIDiTZATCASetupWizard()
    
    def render_wizard_page(self):
        """Render the wizard page with SEIDiT branding"""
        wizard_data = self.wizard.get_wizard_data()
        if not wizard_data:
            self.wizard.create_wizard()
            wizard_data = self.wizard.get_wizard_data()
        
        current_step = wizard_data.current_step
        step_content = self.wizard.get_step_content(current_step)
        
        return {
            'wizard_data': wizard_data,
            'step_content': step_content,
            'current_step': current_step,
            'total_steps': len(self.wizard.steps),
            'step_index': self.wizard.steps.index(current_step) + 1,
            'provider': 'SEIDiT',
            'website': 'https://seidit.com',
            'support_email': 'support@seidit.com'
        }

# ERPNext Page Template with SEIDiT branding
def get_seidit_zatca_wizard_page():
    """Get SEIDiT ZATCA wizard page content"""
    page = SEIDiTZATCAWizardPage()
    return page.render_wizard_page()

# API Endpoints for SEIDiT Wizard
@frappe.whitelist()
def update_seidit_wizard_step(step, data=None):
    """Update SEIDiT wizard step via API"""
    wizard = SEIDiTZATCASetupWizard()
    wizard.update_step(step, json.loads(data) if data else None)
    return {'status': 'success', 'provider': 'SEIDiT'}

@frappe.whitelist()
def test_seidit_zatca_connection():
    """Test ZATCA connection with SEIDiT implementation"""
    try:
        wizard_data = frappe.get_doc("ZATCA Setup Wizard", "Default")
        
        # Test API connection
        import requests
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {wizard_data.api_key}',
            'Accept': 'application/json',
            'User-Agent': 'SEIDiT-ZATCA-Wizard/2.0.0',
            'X-Provider': 'SEIDiT'
        }
        
        test_url = "https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal/test/status"
        response = requests.get(test_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return {
                'status': 'success',
                'message': 'Connection successful! SEIDiT implementation verified.',
                'response': response.json(),
                'provider': 'SEIDiT'
            }
        else:
            return {
                'status': 'error',
                'message': f'Connection failed: {response.status_code}',
                'response': response.text,
                'provider': 'SEIDiT'
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Connection error: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def create_seidit_test_invoice():
    """Create a test invoice for ZATCA testing with SEIDiT branding"""
    try:
        # Check license usage limit
        from seidit_license_system import check_usage_limit
        usage_ok, message = check_usage_limit()
        
        if not usage_ok:
            return {
                'status': 'error',
                'message': f'SEIDiT License Limit: {message}. Please contact zatca@seidit.com for license.',
                'provider': 'SEIDiT'
            }
        
        # Create test customer if not exists
        if not frappe.db.exists("Customer", "SEIDiT Test Customer"):
            frappe.get_doc({
                'doctype': 'Customer',
                'customer_name': 'SEIDiT Test Customer',
                'customer_type': 'Company',
                'customer_group': 'Commercial',
                'territory': 'Saudi Arabia'
            }).insert()
        
        # Create test item if not exists
        if not frappe.db.exists("Item", "SEIDiT Test Item"):
            frappe.get_doc({
                'doctype': 'Item',
                'item_code': 'SEIDiT Test Item',
                'item_name': 'SEIDiT Test Item',
                'item_group': 'Products',
                'stock_uom': 'Nos',
                'is_stock_item': 0
            }).insert()
        
        # Create test invoice
        invoice = frappe.get_doc({
            'doctype': 'Sales Invoice',
            'customer': 'SEIDiT Test Customer',
            'posting_date': now_datetime().date(),
            'due_date': now_datetime().date(),
            'items': [
                {
                    'item_code': 'SEIDiT Test Item',
                    'qty': 1,
                    'rate': 100.00,
                    'amount': 100.00
                }
            ],
            'taxes_and_charges': 'VAT 15% - ZATCA',
            'status': 'Draft'
        })
        
        invoice.insert()
        invoice.submit()
        
        return {
            'status': 'success',
            'message': 'SEIDiT test invoice created successfully!',
            'invoice': invoice.name,
            'provider': 'SEIDiT'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error creating SEIDiT test invoice: {str(e)}',
            'provider': 'SEIDiT'
        }

@frappe.whitelist()
def open_seidit_zatca_portal(environment='test'):
    """Open ZATCA portal in browser with SEIDiT branding"""
    portals = {
        'test': 'https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal/test',
        'live': 'https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal'
    }
    
    url = portals.get(environment, portals['test'])
    webbrowser.open(url)
    
    return {
        'status': 'success',
        'message': f'Opening ZATCA {environment} portal... Powered by SEIDiT',
        'url': url,
        'provider': 'SEIDiT'
    }

@frappe.whitelist()
def get_seidit_installation_info():
    """Get SEIDiT installation information for license"""
    try:
        from seidit_license_system import SEIDiTLicenseSystem
        license_system = SEIDiTLicenseSystem()
        return license_system.get_installation_info()
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error getting installation info: {str(e)}',
            'provider': 'SEIDiT'
        }

# ERPNext Page JavaScript with SEIDiT branding and license warnings
SEIDiT_ZATCA_WIZARD_JS = """
frappe.pages['seidit-zatca-setup-wizard'].page = class extends frappe.views.Page {
    constructor(wrapper) {
        super(wrapper);
        this.page = wrapper.page;
        this.wizard = null;
        this.current_step = 'welcome';
        this.provider = 'SEIDiT';
        this.init();
    }
    
    init() {
        this.load_wizard_data();
        this.render_wizard();
    }
    
    async load_wizard_data() {
        const response = await frappe.call('zatca_setup_wizard.get_seidit_zatca_wizard_page');
        this.wizard_data = response.message;
        this.current_step = this.wizard_data.current_step;
    }
    
    render_wizard() {
        this.page.clear();
        
        const container = $(`
            <div class="seidit-zatca-wizard-container">
                <div class="wizard-header">
                    <div class="provider-branding">
                        <img src="https://seidit.com/logo.png" alt="SEIDiT" class="provider-logo">
                        <h2>SEIDiT ZATCA Phase 2 Setup Wizard</h2>
                        <p class="provider-tagline">Official SEIDiT Implementation</p>
                    </div>
                    <div class="wizard-progress">
                        <span class="step-indicator">Step ${this.wizard_data.step_index} of ${this.wizard_data.total_steps}</span>
                    </div>
                </div>
                <div class="wizard-content">
                    ${this.render_step_content()}
                </div>
                <div class="wizard-actions">
                    ${this.render_actions()}
                </div>
                <div class="provider-footer">
                    <p>Powered by <a href="https://seidit.com" target="_blank">SEIDiT</a> | 
                    <a href="https://seidit.com/support" target="_blank">Support</a> | 
                    <a href="https://seidit.com/zatca/docs" target="_blank">Documentation</a></p>
                </div>
            </div>
        `);
        
        this.page.append(container);
        this.bind_events();
    }
    
    render_step_content() {
        const content = this.wizard_data.step_content;
        let html = `
            <div class="step-content">
                <h3>${content.title}</h3>
                <p>${content.description}</p>
        `;
        
        if (content.instructions) {
            html += '<ul class="instructions">';
            content.instructions.forEach(instruction => {
                html += `<li>${instruction}</li>`;
            });
            html += '</ul>';
        }
        
        if (content.fields) {
            html += '<div class="form-fields">';
            content.fields.forEach(field => {
                html += this.render_field(field);
            });
            html += '</div>';
        }
        
        if (content.portal_links) {
            html += '<div class="portal-links">';
            html += '<h4>ZATCA Portal Links:</h4>';
            html += '<div class="btn-group">';
            html += `<button class="btn btn-secondary" onclick="openPortal('test')">Test Portal</button>`;
            html += `<button class="btn btn-primary" onclick="openPortal('live')">Live Portal</button>`;
            html += '</div>';
            html += '</div>';
        }
        
        if (content.license_info) {
            html += '<div class="license-info">';
            html += '<h4>SEIDiT License Information:</h4>';
            html += '<div class="license-details">';
            html += `<p><strong>Free Limit:</strong> ${content.license_info.free_limit} invoices</p>`;
            html += `<p><strong>Installation ID:</strong> <code>${content.license_info.installation_id}</code></p>`;
            html += `<p><strong>License Required:</strong> ${content.license_info.license_required}</p>`;
            html += '</div>';
            html += '<div class="contact-info">';
            html += '<h5>Contact SEIDiT for License:</h5>';
            html += `<p><strong>Email:</strong> <a href="mailto:${content.contact_info.email}">${content.contact_info.email}</a></p>`;
            html += `<p><strong>WhatsApp:</strong> <a href="https://wa.me/${content.contact_info.whatsapp.replace('+', '')}" target="_blank">${content.contact_info.whatsapp}</a></p>`;
            html += '</div>';
            html += '</div>';
        }
        
        if (content.warning_message) {
            html += `<div class="warning">${content.warning_message}</div>`;
        }
        
        if (content.provider_info) {
            html += '<div class="provider-info">';
            html += '<h4>SEIDiT Support:</h4>';
            html += '<ul>';
            html += `<li><strong>Website:</strong> <a href="${content.provider_info.website}" target="_blank">${content.provider_info.website}</a></li>`;
            html += `<li><strong>Support:</strong> <a href="${content.provider_info.support}" target="_blank">${content.provider_info.support}</a></li>`;
            html += `<li><strong>Email:</strong> <a href="mailto:${content.provider_info.email}">${content.provider_info.email}</a></li>`;
            html += '</ul>';
            html += '</div>';
        }
        
        html += '</div>';
        return html;
    }
    
    render_field(field) {
        let html = `<div class="form-group">`;
        html += `<label>${field.label}</label>`;
        
        if (field.fieldtype === 'Check') {
            html += `<input type="checkbox" name="${field.fieldname}" ${field.default ? 'checked' : ''}>`;
        } else {
            html += `<input type="text" name="${field.fieldname}" placeholder="${field.placeholder || ''}" class="form-control">`;
        }
        
        if (field.help) {
            html += `<small class="help-text">${field.help}</small>`;
        }
        
        html += `</div>`;
        return html;
    }
    
    render_actions() {
        const step_index = this.wizard_data.step_index;
        const total_steps = this.wizard_data.total_steps;
        
        let html = '<div class="wizard-buttons">';
        
        if (step_index > 1) {
            html += '<button class="btn btn-secondary" onclick="previousStep()">Previous</button>';
        }
        
        if (step_index < total_steps) {
            html += '<button class="btn btn-primary" onclick="nextStep()">Next</button>';
        } else {
            html += '<button class="btn btn-success" onclick="completeSetup()">Complete Setup</button>';
        }
        
        html += '</div>';
        return html;
    }
    
    bind_events() {
        // Bind form events
        this.page.find('input, select, textarea').on('change', (e) => {
            this.save_field_data(e.target.name, e.target.value);
        });
    }
    
    async save_field_data(fieldname, value) {
        await frappe.call('zatca_setup_wizard.update_seidit_wizard_step', {
            step: this.current_step,
            data: JSON.stringify({[fieldname]: value})
        });
    }
    
    async next_step() {
        const next_step_index = this.wizard_data.step_index;
        const next_step = this.wizard_data.wizard_data.steps[next_step_index];
        
        await frappe.call('zatca_setup_wizard.update_seidit_wizard_step', {
            step: next_step
        });
        
        this.load_wizard_data();
        this.render_wizard();
    }
    
    async previous_step() {
        const prev_step_index = this.wizard_data.step_index - 2;
        const prev_step = this.wizard_data.wizard_data.steps[prev_step_index];
        
        await frappe.call('zatca_setup_wizard.update_seidit_wizard_step', {
            step: prev_step
        });
        
        this.load_wizard_data();
        this.render_wizard();
    }
    
    async test_connection() {
        const result = await frappe.call('zatca_setup_wizard.test_seidit_zatca_connection');
        
        if (result.message.status === 'success') {
            frappe.show_alert('✅ SEIDiT connection successful!', 'success');
        } else {
            frappe.show_alert(`❌ SEIDiT connection failed: ${result.message.message}`, 'error');
        }
    }
    
    async create_test_invoice() {
        const result = await frappe.call('zatca_setup_wizard.create_seidit_test_invoice');
        
        if (result.message.status === 'success') {
            frappe.show_alert('✅ SEIDiT test invoice created successfully!', 'success');
        } else {
            frappe.show_alert(`❌ SEIDiT Error: ${result.message.message}`, 'error');
        }
    }
    
    async open_portal(environment) {
        await frappe.call('zatca_setup_wizard.open_seidit_zatca_portal', {
            environment: environment
        });
    }
    
    async get_installation_info() {
        const result = await frappe.call('zatca_setup_wizard.get_seidit_installation_info');
        return result.message;
    }
};

// Global functions for button clicks
window.nextStep = function() {
    frappe.pages['seidit-zatca-setup-wizard'].page.next_step();
};

window.previousStep = function() {
    frappe.pages['seidit-zatca-setup-wizard'].page.previous_step();
};

window.testConnection = function() {
    frappe.pages['seidit-zatca-setup-wizard'].page.test_connection();
};

window.createTestInvoice = function() {
    frappe.pages['seidit-zatca-setup-wizard'].page.create_test_invoice();
};

window.openPortal = function(environment) {
    frappe.pages['seidit-zatca-setup-wizard'].page.open_portal(environment);
};

window.completeSetup = function() {
    frappe.pages['seidit-zatca-setup-wizard'].page.complete_setup();
};

window.getInstallationInfo = function() {
    frappe.pages['seidit-zatca-setup-wizard'].page.get_installation_info();
};
"""

# ERPNext Page CSS with SEIDiT branding and license styling
SEIDiT_ZATCA_WIZARD_CSS = """
.seidit-zatca-wizard-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.wizard-header {
    text-align: center;
    margin-bottom: 30px;
    padding: 30px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    color: white;
}

.provider-branding {
    margin-bottom: 20px;
}

.provider-logo {
    height: 60px;
    margin-bottom: 15px;
}

.wizard-header h2 {
    color: white;
    margin-bottom: 10px;
    font-size: 28px;
    font-weight: 600;
}

.provider-tagline {
    color: rgba(255,255,255,0.9);
    font-size: 16px;
    margin-bottom: 20px;
}

.wizard-progress {
    font-size: 16px;
    color: rgba(255,255,255,0.9);
}

.step-indicator {
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 8px 20px;
    border-radius: 25px;
    font-weight: bold;
    backdrop-filter: blur(10px);
}

.wizard-content {
    background: white;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.step-content h3 {
    color: #2c3e50;
    margin-bottom: 20px;
    font-size: 24px;
    font-weight: 600;
}

.step-content p {
    color: #34495e;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.instructions {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
    color: white;
}

.instructions li {
    margin-bottom: 12px;
    color: white;
    font-weight: 500;
}

.form-fields {
    margin: 25px 0;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #2c3e50;
    font-size: 14px;
}

.form-control {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #e1e8ed;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.3s ease;
}

.form-control:focus {
    border-color: #667eea;
    outline: none;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.help-text {
    display: block;
    margin-top: 6px;
    color: #7f8c8d;
    font-size: 12px;
    font-style: italic;
}

.portal-links {
    margin: 25px 0;
    padding: 20px;
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border-radius: 8px;
}

.portal-links h4 {
    margin-bottom: 15px;
    color: #2c3e50;
    font-weight: 600;
}

.btn-group {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    display: inline-block;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-secondary {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
}

.btn-success {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.wizard-actions {
    text-align: center;
    margin-top: 30px;
}

.wizard-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}

.license-info {
    margin: 25px 0;
    padding: 25px;
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border-radius: 8px;
    border: 2px solid #f39c12;
}

.license-info h4 {
    margin-bottom: 20px;
    color: #2c3e50;
    font-weight: 600;
    font-size: 18px;
}

.license-details {
    margin-bottom: 20px;
}

.license-details p {
    margin-bottom: 10px;
    color: #34495e;
    font-weight: 500;
}

.license-details code {
    background: rgba(255,255,255,0.3);
    padding: 4px 8px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-weight: bold;
}

.contact-info {
    background: rgba(255,255,255,0.2);
    padding: 15px;
    border-radius: 6px;
}

.contact-info h5 {
    margin-bottom: 10px;
    color: #2c3e50;
    font-weight: 600;
}

.contact-info p {
    margin-bottom: 8px;
    color: #34495e;
}

.contact-info a {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.contact-info a:hover {
    text-decoration: underline;
}

.provider-info {
    margin: 25px 0;
    padding: 20px;
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border-radius: 8px;
}

.provider-info h4 {
    margin-bottom: 15px;
    color: #2c3e50;
    font-weight: 600;
}

.provider-info ul {
    list-style: none;
    padding: 0;
}

.provider-info li {
    margin-bottom: 8px;
    color: #34495e;
}

.provider-info a {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.provider-info a:hover {
    text-decoration: underline;
}

.provider-footer {
    text-align: center;
    margin-top: 30px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
    color: #6c757d;
    font-size: 14px;
}

.provider-footer a {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.provider-footer a:hover {
    text-decoration: underline;
}

.warning {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border: 2px solid #f39c12;
    color: #d68910;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
    font-weight: 500;
    font-size: 16px;
}

.success-message {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border: 2px solid #27ae60;
    color: #155724;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
    font-weight: 500;
}

@media (max-width: 768px) {
    .seidit-zatca-wizard-container {
        padding: 10px;
    }
    
    .wizard-content {
        padding: 20px;
    }
    
    .btn-group {
        flex-direction: column;
    }
    
    .wizard-buttons {
        flex-direction: column;
        align-items: center;
    }
}
""" 