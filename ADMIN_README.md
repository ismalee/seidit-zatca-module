# SEIDiT License Administration System

## Overview

**SEIDiT License Administration System** is a private, secure licensing management platform for SEIDiT's ZATCA module. This system handles license generation, customer management, revenue tracking, and usage analytics.

## ⚠️ **PRIVATE REPOSITORY**

This repository contains **confidential SEIDiT licensing infrastructure**. 
- **DO NOT** share this repository publicly
- **DO NOT** commit sensitive keys or credentials
- **DO NOT** expose admin endpoints publicly

## Features

### 🔐 **License Management**
- ✅ **License Generation** - Create secure licenses
- ✅ **Customer Database** - Manage customer information
- ✅ **Installation Tracking** - Monitor license usage
- ✅ **License Revocation** - Revoke compromised licenses

### 💰 **Revenue Tracking**
- ✅ **Payment Management** - Track customer payments
- ✅ **Revenue Analytics** - Generate revenue reports
- ✅ **Invoice Generation** - Create customer invoices
- ✅ **Payment History** - Complete payment records

### 📊 **Usage Analytics**
- ✅ **License Validation** - Track validation attempts
- ✅ **Usage Patterns** - Monitor customer usage
- ✅ **Error Tracking** - Log and analyze errors
- ✅ **Performance Metrics** - System performance monitoring

### 🛡️ **Security Features**
- ✅ **Multi-layer Encryption** - Advanced encryption
- ✅ **Hardware Binding** - License-to-hardware binding
- ✅ **Anti-Reverse Engineering** - Protection mechanisms
- ✅ **Server-side Validation** - Remote license verification

## Installation

### **Server Setup**
```bash
# 1. Clone repository (PRIVATE)
git clone https://github.com/ismalee/seidit-license-admin.git
cd seidit-license-admin

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Initialize database
python init_database.py

# 5. Start license server
python seidit_license_server_api.py
```

### **ERPNext Integration**
```bash
# 1. Install admin module in ERPNext
bench --site seidit.com install-app seidit_license_admin

# 2. Run migrations
bench --site seidit.com migrate

# 3. Restart ERPNext
bench restart
```

## Configuration

### **Environment Variables**
```bash
# .env file
SEIDIT_SERVER_KEY=your_server_key_here
SEIDIT_SECRET_KEY=your_secret_key_here
SEIDIT_PROVIDER=SEIDiT
SEIDIT_VERSION=2.0.0
DATABASE_URL=mysql://user:pass@localhost/seidit_licenses
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

### **Domain Configuration**
```bash
# Point license.seidit.com to your server
# A record: license.seidit.com → Your Server IP
```

## API Endpoints

### **License Management**
```
POST /api/v1/validate          # Validate license
POST /api/v1/generate          # Generate license (admin)
POST /api/v1/revoke           # Revoke license (admin)
GET  /api/v1/status           # Server status
```

### **Customer Management**
```
POST /api/v1/customers        # Create customer
GET  /api/v1/customers        # List customers
PUT  /api/v1/customers/:id    # Update customer
DELETE /api/v1/customers/:id  # Delete customer
```

### **Revenue Tracking**
```
POST /api/v1/revenue          # Add revenue entry
GET  /api/v1/revenue          # Get revenue report
GET  /api/v1/analytics        # Usage analytics
```

## Database Schema

### **Licenses Table**
```sql
CREATE TABLE `tabSEIDiT License` (
    `name` varchar(140) PRIMARY KEY,
    `license_key` text NOT NULL,
    `installation_id` varchar(140) NOT NULL,
    `customer_id` varchar(140) NOT NULL,
    `license_type` varchar(20) DEFAULT 'lifetime',
    `status` varchar(20) DEFAULT 'Active',
    `created_at` datetime,
    `expires_at` datetime,
    `last_validated` datetime,
    `validation_count` int DEFAULT 0,
    `features` text,
    `signature` varchar(255)
);
```

### **Customers Table**
```sql
CREATE TABLE `tabSEIDiT Customer` (
    `name` varchar(140) PRIMARY KEY,
    `customer_id` varchar(140) UNIQUE NOT NULL,
    `company_name` varchar(140) NOT NULL,
    `contact_person` varchar(140),
    `email` varchar(140),
    `phone` varchar(20),
    `address` text,
    `country` varchar(50),
    `status` varchar(20) DEFAULT 'active',
    `created_at` datetime
);
```

### **Usage Logs Table**
```sql
CREATE TABLE `tabSEIDiT License Log` (
    `name` varchar(140) PRIMARY KEY,
    `license_key` varchar(140) NOT NULL,
    `customer_id` varchar(140) NOT NULL,
    `action` varchar(50) NOT NULL,
    `timestamp` datetime,
    `ip_address` varchar(45),
    `user_agent` text,
    `invoice_count` int DEFAULT 0
);
```

## Admin Functions

### **License Generation**
```python
# Generate license for customer
from seidit_license_admin import SEIDiTLicenseAdmin

admin = SEIDiTLicenseAdmin()
result = admin.generate_license_for_customer(
    customer_id="CUST001",
    installation_id="INST001",
    license_type="lifetime"
)
```

### **Customer Management**
```python
# Create new customer
customer_data = {
    'company_name': 'ABC Company',
    'contact_person': 'John Doe',
    'email': 'john@abc.com',
    'phone': '+966-XX-XXXXXXX',
    'address': 'Riyadh, Saudi Arabia',
    'country': 'Saudi Arabia'
}

result = admin.create_customer(customer_data)
```

### **Revenue Tracking**
```python
# Add revenue entry
result = admin.add_revenue_entry(
    customer_id="CUST001",
    license_key="LICENSE_KEY_HERE",
    amount=1000.00,
    currency="USD",
    payment_method="bank_transfer"
)
```

## Security Measures

### **Encryption**
- **Multi-layer encryption** for license keys
- **Hardware fingerprinting** for license binding
- **Time-based keys** for additional security
- **HMAC signatures** for data integrity

### **Access Control**
- **Admin-only endpoints** for sensitive operations
- **Request signing** for API authentication
- **IP whitelisting** for admin access
- **Session management** for admin users

### **Monitoring**
- **Usage analytics** for license monitoring
- **Error tracking** for system health
- **Performance metrics** for optimization
- **Security alerts** for suspicious activity

## Backup and Recovery

### **Database Backup**
```bash
# Daily backup script
mysqldump -u user -p seidit_licenses > backup_$(date +%Y%m%d).sql

# Automated backup
0 2 * * * /path/to/backup_script.sh
```

### **Configuration Backup**
```bash
# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env *.py *.json
```

## Monitoring

### **System Health**
- **Server uptime** monitoring
- **Database performance** tracking
- **API response times** monitoring
- **Error rate** tracking

### **License Analytics**
- **Active licenses** count
- **Validation frequency** tracking
- **Revenue trends** analysis
- **Customer usage** patterns

## Troubleshooting

### **Common Issues**

1. **License Validation Failed**
   ```bash
   # Check server logs
   tail -f /var/log/seidit_license_server.log
   
   # Verify database connection
   mysql -u user -p seidit_licenses -e "SELECT 1"
   ```

2. **Database Connection Error**
   ```bash
   # Check MySQL service
   systemctl status mysql
   
   # Verify credentials
   mysql -u user -p -e "USE seidit_licenses"
   ```

3. **SSL Certificate Issues**
   ```bash
   # Check certificate validity
   openssl x509 -in cert.pem -text -noout
   
   # Test SSL connection
   openssl s_client -connect license.seidit.com:443
   ```

## Support

### **Internal Support**
- **Technical Issues**: tech@seidit.com
- **License Issues**: licenses@seidit.com
- **Security Issues**: security@seidit.com

### **Emergency Contact**
- **24/7 Support**: +966-XX-XXXXXXX
- **Emergency Email**: emergency@seidit.com

## Changelog

### **Version 2.0.0**
- ✅ Multi-layer encryption system
- ✅ Hardware binding implementation
- ✅ Advanced protection mechanisms
- ✅ Comprehensive analytics

### **Version 1.0.0**
- ✅ Basic license management
- ✅ Customer database
- ✅ Revenue tracking
- ✅ Usage analytics

---

**Copyright (c) 2024 SEIDiT (https://seidit.com). All rights reserved.**

This is a private repository containing confidential SEIDiT licensing infrastructure. 