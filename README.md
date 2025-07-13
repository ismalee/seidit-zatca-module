# SEIDiT ZATCA Phase 2 Module for ERPNext

## Overview

**SEIDiT ZATCA Phase 2 Module** is a comprehensive e-invoicing solution for ERPNext that provides full compliance with Saudi Arabia's ZATCA (Zakat, Tax and Customs Authority) Phase 2 requirements.

## Features

### 🏢 **ZATCA Compliance**
- ✅ **XML Generation** - Compliant invoice XML creation
- ✅ **QR Code Generation** - ZATCA-compliant QR codes
- ✅ **Cryptographic Signing** - Digital signature implementation
- ✅ **API Integration** - Direct ZATCA API communication
- ✅ **Invoice Processing** - Automatic invoice submission

### 🔐 **Secure Licensing**
- ✅ **Hardware Binding** - Licenses tied to specific installations
- ✅ **Server Validation** - Remote license verification
- ✅ **Usage Tracking** - Monitor invoice generation
- ✅ **Anti-Reverse Engineering** - Advanced protection mechanisms

### 🎯 **Easy Setup**
- ✅ **Setup Wizard** - Step-by-step configuration
- ✅ **API Credentials** - Secure credential management
- ✅ **Test Mode** - Safe testing environment
- ✅ **Live Mode** - Production deployment

## Installation

### **Quick Install**
```bash
# Download the module
wget https://github.com/ismalee/seidit-zatca-module/archive/main.zip
unzip main.zip

# Run installation script
python install_seidit_complete.py
```

### **Manual Install**
```bash
# 1. Copy files to ERPNext apps directory
cp -r seidit_zatca_module /path/to/erpnext/apps/

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run ERPNext migrations
bench migrate

# 4. Restart ERPNext
bench restart
```

## Setup Wizard

### **Step 1: Access Setup Wizard**
1. Go to **SEIDiT ZATCA Setup Wizard** in ERPNext
2. Click **"Start Setup"**

### **Step 2: Get Installation ID**
1. Copy your **Installation ID**
2. Contact SEIDiT for license: **support@seidit.com**

### **Step 3: Configure ZATCA**
1. Get API credentials from **ZATCA Portal**
2. Enter credentials in setup wizard
3. Test connection

### **Step 4: Activate License**
1. Enter your SEIDiT license key
2. Activate license
3. Switch to **Live Mode**

## Configuration

### **ZATCA Settings**
```python
# Required Settings
- Company Tax Number
- ZATCA API Credentials
- Certificate Path
- Private Key Path
```

### **License Settings**
```python
# License Configuration
- SEIDiT License Key
- Installation ID
- License Status
- Usage Limits
```

## Usage

### **Generate ZATCA Invoice**
```python
# In ERPNext Sales Invoice
1. Create/Edit Sales Invoice
2. Fill required ZATCA fields
3. Click "Generate ZATCA XML"
4. Submit to ZATCA
```

### **Check Invoice Status**
```python
# Monitor invoice status
1. Go to ZATCA Logs
2. Check submission status
3. View ZATCA responses
```

## API Endpoints

### **License Validation**
```
POST /api/method/seidit_license_system.validate_license
```

### **ZATCA Invoice Submission**
```
POST /api/method/zatca_phase2_module.submit_invoice
```

### **Setup Wizard**
```
GET /api/method/zatca_setup_wizard.get_installation_info
```

## Security Features

### **License Protection**
- **Hardware Fingerprinting** - Binds to specific hardware
- **Server Validation** - Remote license verification
- **Anti-Debugging** - Detects reverse engineering tools
- **Code Obfuscation** - Protects sensitive code

### **ZATCA Security**
- **Cryptographic Signing** - Digital signatures
- **Secure API Communication** - Encrypted API calls
- **Certificate Management** - Secure certificate handling

## Support

### **SEIDiT Support**
- **Email**: support@seidit.com
- **Phone**: +966-XX-XXXXXXX
- **Website**: https://seidit.com
- **Support Hours**: 24/7

### **Documentation**
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **API Documentation**: [API_DOCS.md](API_DOCS.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## License

### **SEIDiT License Agreement**
- **Free Trial**: 10 invoices
- **Paid License**: Unlimited invoices
- **Support**: Premium support included
- **Updates**: Regular updates and patches

### **Terms**
- **Usage**: Single ERPNext installation
- **Transfer**: License transfer requires SEIDiT approval
- **Modification**: No modification allowed
- **Distribution**: No redistribution allowed

## Changelog

### **Version 2.0.0**
- ✅ Multi-layer encryption
- ✅ Hardware binding
- ✅ Server-side validation
- ✅ Advanced protection mechanisms

### **Version 1.0.0**
- ✅ Basic ZATCA compliance
- ✅ XML generation
- ✅ QR code creation
- ✅ API integration

## Contributing

This is a **proprietary module** by SEIDiT. No contributions are accepted.

## Contact

### **SEIDiT**
- **Website**: https://seidit.com
- **Email**: info@seidit.com
- **Address**: Saudi Arabia

---

**Copyright (c) 2024 SEIDiT (https://seidit.com). All rights reserved.**

This module is proprietary to SEIDiT and protected by intellectual property laws. 