# SEIDiT ZATCA Module Deployment Guide

## 🚀 **Production Deployment for SEIDiT**

### **Server Configuration:**
- **ERPNext Server IP**: `154.90.50.194`
- **SEIDiT Domain**: `seidit.com` (Hostinger)
- **License Subdomain**: `license.seidit.com` (Point to ERPNext server)

---

## 📋 **Step 1: Domain Configuration**

### **Configure DNS Records:**
```
# Add A record in Hostinger DNS
license.seidit.com → 154.90.50.194
```

### **SSL Certificate:**
```bash
# On ERPNext server (154.90.50.194)
# Install SSL certificate for license.seidit.com
sudo certbot --nginx -d license.seidit.com
```

---

## 📦 **Step 2: Deploy Public Module (Customer Distribution)**

### **Push to GitHub:**
```bash
cd seidit-zatca-module
git add .
git commit -m "Updated for production deployment"
git push origin main
```

### **Customer Installation:**
```bash
# Customers will install from:
https://github.com/ismalee/seidit-zatca-module

# Installation command:
python install_seidit_complete.py
```

---

## 🔐 **Step 3: Deploy Private Admin Module (SEIDiT Server)**

### **On ERPNext Server (154.90.50.194):**

```bash
# 1. Clone private repository
git clone https://github.com/ismalee/seidit-license-admin.git
cd seidit-license-admin

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install in ERPNext
bench --site seidit.com install-app seidit_license_admin
bench --site seidit.com migrate

# 4. Restart ERPNext
bench restart
```

### **Configure Environment:**
```bash
# Create .env file
cat > .env << EOF
SEIDIT_SERVER_KEY=your_server_key_here
SEIDIT_SECRET_KEY=your_secret_key_here
SEIDIT_PROVIDER=SEIDiT
SEIDIT_VERSION=2.0.0
DATABASE_URL=mysql://user:pass@localhost/seidit_licenses
SSL_CERT_PATH=/etc/letsencrypt/live/license.seidit.com/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/license.seidit.com/privkey.pem
EOF
```

---

## ⚙️ **Step 4: Server Configuration**

### **Firewall Setup:**
```bash
# Allow license server port
sudo ufw allow 5000
sudo ufw allow 443
sudo ufw allow 80
```

### **Nginx Configuration:**
```nginx
# /etc/nginx/sites-available/license.seidit.com
server {
    listen 80;
    server_name license.seidit.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name license.seidit.com;
    
    ssl_certificate /etc/letsencrypt/live/license.seidit.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/license.seidit.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **Enable Site:**
```bash
sudo ln -s /etc/nginx/sites-available/license.seidit.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🚀 **Step 5: Start License Server**

### **Run License Server:**
```bash
# Start the license server
cd seidit-license-admin
python seidit_license_server_api.py
```

### **Test Server:**
```bash
# Test server status
curl https://license.seidit.com/api/v1/status
```

---

## 📊 **Step 6: Admin Panel Setup**

### **Access Admin Panel:**
1. Go to ERPNext: `https://154.90.50.194`
2. Login as Administrator
3. Look for "SEIDiT License Admin" in the menu

### **Initial Setup:**
1. **Create Customer**: Add customer information
2. **Generate License**: Create license for customer
3. **Monitor Usage**: Track license validations
4. **Revenue Tracking**: Monitor payments

---

## 🔧 **Step 7: Testing**

### **Test License Validation:**
```bash
# Test from customer server
curl -X POST https://license.seidit.com/api/v1/validate \
  -H "Content-Type: application/json" \
  -H "X-SEIDiT-Signature: your_signature" \
  -d '{
    "license_key": "test_license_key",
    "installation_id": "test_installation_id"
  }'
```

### **Test Admin Functions:**
```bash
# Generate license
curl -X POST https://license.seidit.com/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "installation_id": "CUST001",
    "customer_info": {"company": "Test Company"}
  }'
```

---

## 📈 **Step 8: Monitoring**

### **Server Monitoring:**
```bash
# Check server status
systemctl status nginx
systemctl status mysql

# Monitor logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### **License Analytics:**
- Monitor license validations
- Track usage patterns
- Monitor revenue
- Check for abuse

---

## 🔒 **Step 9: Security**

### **Security Checklist:**
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Database encrypted
- [ ] Admin access restricted
- [ ] Monitoring enabled
- [ ] Backups configured

### **Regular Maintenance:**
```bash
# Update SSL certificate
sudo certbot renew

# Update system
sudo apt update && sudo apt upgrade

# Backup database
mysqldump -u user -p seidit_licenses > backup_$(date +%Y%m%d).sql
```

---

## 📞 **Step 10: Support Setup**

### **Support Information:**
- **Website**: https://seidit.com
- **Support Email**: support@seidit.com
- **WhatsApp**: +966567414356
- **Documentation**: https://seidit.com/zatca/docs

### **Customer Support:**
1. **Installation Support**: Help customers install module
2. **Configuration Support**: Assist with ZATCA setup
3. **License Support**: Handle license issues
4. **Technical Support**: Resolve technical problems

---

## ✅ **Deployment Complete!**

### **What's Ready:**
- ✅ **Public Module**: Available for customer download
- ✅ **Private Admin**: Installed on ERPNext server
- ✅ **License Server**: Running on `license.seidit.com`
- ✅ **Domain Configuration**: Pointing to ERPNext server
- ✅ **SSL Certificate**: Secure HTTPS connections
- ✅ **Admin Panel**: Ready for license management

### **Next Steps:**
1. **Test everything** thoroughly
2. **Create first customer** in admin panel
3. **Generate first license** for testing
4. **Launch marketing** for customers
5. **Monitor usage** and revenue

---

**🎉 Your SEIDiT ZATCA licensing system is now production-ready!**

**Server**: `154.90.50.194`  
**Domain**: `license.seidit.com`  
**Status**: ✅ **DEPLOYED** 