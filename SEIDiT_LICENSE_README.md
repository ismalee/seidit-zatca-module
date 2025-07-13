# SEIDiT Secure Licensing System

## Overview

This is a **complete secure licensing system** for SEIDiT's ZATCA Phase 2 module. The system includes multiple layers of protection against reverse engineering, tampering, and unauthorized use.

## Security Features

### 🔐 Multi-Layer Encryption
- **Layer 1**: Basic Fernet encryption
- **Layer 2**: Hardware-bound AES encryption
- **Layer 3**: Time-based encryption
- **Hardware Fingerprinting**: Binds licenses to specific hardware
- **Anti-Reverse Engineering**: Code obfuscation and protection

### 🛡️ Protection Mechanisms
- **Anti-Debugging**: Detects debugging tools and virtual machines
- **Code Integrity**: Checks for code tampering
- **Environment Protection**: Validates execution environment
- **Runtime Protection**: Continuous validation during execution

### 🌐 Server-Side Validation
- **Remote License Server**: Validates licenses against SEIDiT's servers
- **Blacklist System**: Prevents revoked licenses from working
- **Usage Analytics**: Tracks license usage and abuse
- **Real-time Validation**: Every license check validates with server

## Components

### 1. License Server (`seidit_license_server_api.py`)
**Deploy this on SEIDiT's servers**

```bash
# Install dependencies
pip install flask flask-cors cryptography

# Run the server
python seidit_license_server_api.py
```

**Features:**
- License generation and validation
- Customer database management
- Usage tracking and analytics
- Blacklist management
- Revenue tracking

### 2. Secure License Client (`seidit_secure_license_server.py`)
**Integrated into ERPNext module**

**Features:**
- Multi-layer encryption/decryption
- Hardware fingerprinting
- Anti-reverse engineering protection
- Remote server validation

### 3. License Protection (`seidit_license_protection.py`)
**Advanced protection mechanisms**

**Features:**
- Code obfuscation
- Anti-debugging checks
- Environment validation
- Runtime protection

### 4. License Administration (`seidit_license_admin.py`)
**SEIDiT's internal administration system**

**Features:**
- Customer management
- License generation
- Usage analytics
- Revenue reporting
- License revocation

### 5. Advanced Encryption (`seidit_license_encryption.py`)
**Multi-layer encryption system**

**Features:**
- Hardware-bound encryption
- Time-based keys
- Code obfuscation
- Anti-decompilation

## Deployment Instructions

### For SEIDiT (License Server)

1. **Deploy License Server**
   ```bash
   # On SEIDiT's servers
   git clone <seidit-license-server>
   cd seidit-license-server
   pip install -r requirements.txt
   python seidit_license_server_api.py
   ```

2. **Configure SSL Certificate**
   ```bash
   # Use proper SSL certificate for production
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
   ```

3. **Set up Database**
   ```bash
   # The server automatically creates SQLite database
   # For production, use PostgreSQL or MySQL
   ```

### For Customers (ERPNext Integration)

1. **Install SEIDiT Module**
   ```bash
   # In ERPNext installation
   bench get-app seidit_zatca_module
   bench install-app seidit_zatca_module
   ```

2. **Run Setup Wizard**
   - Navigate to SEIDiT ZATCA Setup Wizard
   - Enter installation ID
   - Contact SEIDiT for license
   - Activate license

## Security Measures

### Against Reverse Engineering

1. **Code Obfuscation**
   ```python
   # Original code is obfuscated
   def check_license():
       return "obfuscated_function"
   ```

2. **Anti-Debugging**
   ```python
   # Detects debugging tools
   if hasattr(sys, 'gettrace') and sys.gettrace():
       return False
   ```

3. **Hardware Binding**
   ```python
   # License bound to specific hardware
   hardware_fingerprint = get_hardware_fingerprint()
   ```

### Against Tampering

1. **Code Integrity Checks**
   ```python
   # Verifies code hasn't been modified
   expected_hash = "pre_calculated_hash"
   actual_hash = calculate_code_hash()
   ```

2. **Signature Verification**
   ```python
   # HMAC signatures prevent tampering
   signature = hmac.new(key, data, hashlib.sha256)
   ```

### Against Unauthorized Use

1. **Server-Side Validation**
   ```python
   # Every license check validates with server
   response = requests.post(license_server_url, data=license_data)
   ```

2. **Blacklist System**
   ```python
   # Revoked licenses are blacklisted
   if installation_id in blacklist:
       return False
   ```

## License Types

### Free Trial (10 Invoices)
- Limited to 10 invoices
- No server validation required
- Basic features only

### Paid License (Unlimited)
- Unlimited invoices
- Server-side validation
- All features included
- Premium support

## API Endpoints

### License Server (SEIDiT)

```
POST /api/v1/validate
POST /api/v1/generate
POST /api/v1/revoke
GET  /api/v1/status
```

### Client API (ERPNext)

```
POST /api/method/seidit_license_system.validate_license
POST /api/method/seidit_license_system.get_installation_info
GET  /api/method/seidit_license_system.check_license_status
```

## Monitoring and Analytics

### Usage Analytics
- License validation frequency
- Invoice generation tracking
- Error monitoring
- Performance metrics

### Revenue Tracking
- License sales
- Customer payments
- Revenue reports
- Payment history

## Support and Maintenance

### For SEIDiT
1. **License Management**: Use admin panel to manage licenses
2. **Customer Support**: Monitor usage and provide support
3. **Security Updates**: Regular security patches and updates
4. **Server Maintenance**: Monitor server health and performance

### For Customers
1. **Setup Support**: Help with initial setup and configuration
2. **Technical Support**: Resolve technical issues
3. **License Renewal**: Handle license renewals and upgrades
4. **Training**: Provide training and documentation

## Security Best Practices

### For SEIDiT
1. **Regular Security Audits**: Monthly security reviews
2. **Encryption Key Rotation**: Rotate keys quarterly
3. **Server Hardening**: Secure server configuration
4. **Backup and Recovery**: Regular backups and disaster recovery

### For Customers
1. **Secure Installation**: Follow security guidelines
2. **Regular Updates**: Keep module updated
3. **Access Control**: Limit access to licensed users
4. **Monitoring**: Monitor for suspicious activity

## Compliance and Legal

### License Agreement
- **Usage Terms**: Clear usage terms and conditions
- **Intellectual Property**: SEIDiT retains all IP rights
- **Liability**: Clear liability limitations
- **Termination**: License termination procedures

### Data Protection
- **Privacy**: Customer data protection
- **GDPR Compliance**: European data protection compliance
- **Data Retention**: Clear data retention policies
- **Security**: Data security measures

## Troubleshooting

### Common Issues

1. **License Validation Failed**
   - Check internet connection
   - Verify license key
   - Contact SEIDiT support

2. **Hardware Binding Error**
   - Hardware changed significantly
   - Contact SEIDiT for license transfer

3. **Server Connection Error**
   - Check firewall settings
   - Verify server URL
   - Contact SEIDiT support

### Debug Mode
```python
# Enable debug mode for troubleshooting
frappe.set_user("Administrator")
frappe.db.set_value("ZATCA Settings", "Default", "debug_mode", 1)
```

## Contact Information

### SEIDiT Support
- **Email**: support@seidit.com
- **Phone**: +966-XX-XXXXXXX
- **Website**: https://seidit.com
- **Support Hours**: 24/7

### Emergency Contact
- **Technical Issues**: tech@seidit.com
- **License Issues**: licenses@seidit.com
- **Security Issues**: security@seidit.com

---

**Copyright (c) 2024 SEIDiT (https://seidit.com). All rights reserved.**

This licensing system is proprietary to SEIDiT and protected by intellectual property laws. Unauthorized copying, modification, or distribution is strictly prohibited. 