# 🚀 ZATCA Phase 2 Setup Wizard - User Guide

## 📋 What You'll Get

✅ **Complete ZATCA Phase 2 Compliance**  
✅ **Step-by-Step Setup Wizard**  
✅ **Automatic Invoice Processing**  
✅ **Test & Live Mode Support**  
✅ **Easy API Credential Management**  

---

## 🎯 Quick Start (5 Minutes)

### Step 1: Access the Wizard
1. Open ERPNext
2. Look for **"ZATCA Setup Wizard"** in the menu
3. Click to open the wizard

### Step 2: Follow the Wizard
The wizard will guide you through 8 simple steps:

#### **Step 1: Welcome** 📝
- Read the overview
- Click **"Next"**

#### **Step 2: VAT Registration** 🏢
- Enter your **15-digit VAT number**
- Enter your **company name**
- Click **"Next"**

#### **Step 3: ZATCA Portal Access** 🌐
- Click **"Test Portal"** (for testing)
- Login with your VAT credentials
- Navigate to **Developer Portal**
- Click **"Next"**

#### **Step 4: API Credentials** 🔑
- Copy **API Key** from ZATCA portal
- Copy **Secret Key** from ZATCA portal
- Keep **"Test Mode"** checked
- Click **"Next"**

#### **Step 5: Test Connection** ✅
- Click **"Test Connection"**
- Verify connection is successful
- Click **"Next"**

#### **Step 6: Live Activation** 🚀
- Uncheck **"Test Mode"**
- Update with **live API credentials**
- Click **"Next"**

#### **Step 7: Invoice Testing** 📄
- Click **"Create Test Invoice"**
- Verify invoice is processed
- Click **"Next"**

#### **Step 8: Completion** 🎉
- Setup is complete!
- Start creating real invoices

---

## 🔧 Getting API Credentials from ZATCA

### For Test Environment:
1. Go to: **https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal/test**
2. Login with your VAT credentials
3. Navigate to **"Developer Portal"**
4. Click **"Generate API Credentials"**
5. Copy **API Key** and **Secret Key**

### For Live Environment:
1. Go to: **https://gw-fatoorah.zatca.gov.sa/e-invoicing/developer-portal**
2. Login with your VAT credentials
3. Navigate to **"Developer Portal"**
4. Click **"Generate API Credentials"**
5. Copy **API Key** and **Secret Key**

---

## 📊 What Happens After Setup

### Automatic Processing:
- ✅ Invoices are processed when submitted
- ✅ QR codes are generated automatically
- ✅ Digital signatures are applied
- ✅ Reports are sent to ZATCA
- ✅ Status is updated in ERPNext

### What You'll See:
- **ZATCA Status** field in invoices
- **QR Code** data in invoices
- **Clearance Status** updates
- **Processing logs** in ZATCA Logs

---

## 🧪 Testing Your Setup

### Test Mode (Recommended First):
1. Keep **"Test Mode"** enabled
2. Create a test invoice
3. Submit the invoice
4. Check **ZATCA Status** field
5. Verify **QR Code** is generated
6. Check **ZATCA Logs** for details

### Live Mode:
1. Disable **"Test Mode"**
2. Update with **live API credentials**
3. Create a real invoice
4. Submit and monitor status
5. Check clearance reports

---

## 🔍 Monitoring & Troubleshooting

### Check Status:
- **ZATCA Settings** → View configuration
- **ZATCA Logs** → View processing history
- **Sales Invoice** → Check ZATCA fields

### Common Issues:

#### ❌ "Connection Failed"
- Check internet connection
- Verify API credentials
- Ensure correct portal URL

#### ❌ "VAT Number Invalid"
- Verify 15-digit format
- Check VAT registration
- Contact ZATCA support

#### ❌ "Invoice Processing Failed"
- Check invoice data
- Verify tax calculations
- Review error logs

---

## 📞 Getting Help

### In ERPNext:
- Check **ZATCA Logs** for errors
- Review **ZATCA Settings**
- Look at invoice **ZATCA fields**

### External Resources:
- **ZATCA Portal**: https://gw-fatoorah.zatca.gov.sa
- **ZATCA Support**: Available in portal
- **ERPNext Docs**: Check system logs

---

## ⚠️ Important Notes

### Before Going Live:
- ✅ Test thoroughly in test mode
- ✅ Verify VAT registration
- ✅ Check API credentials
- ✅ Test with sample invoices
- ✅ Monitor first few live invoices

### Compliance Requirements:
- 📅 Report within 24 hours
- 🔢 Sequential invoice numbering
- 💰 Proper VAT calculations
- 📱 QR code on invoices
- 🔐 Digital signatures

---

## 🎯 Success Checklist

- [ ] Wizard completed successfully
- [ ] API credentials configured
- [ ] Test connection successful
- [ ] Test invoice processed
- [ ] QR code generated
- [ ] Live mode activated (if ready)
- [ ] Real invoice tested
- [ ] Clearance status received

---

## 🚀 You're Ready!

Once you complete the wizard:
1. **Create invoices** normally in ERPNext
2. **Submit invoices** to trigger ZATCA processing
3. **Monitor status** in invoice ZATCA fields
4. **Check logs** for any issues
5. **Enjoy** automatic ZATCA compliance! 🎉

---

*Need help? Check the ZATCA Logs or contact your ERPNext administrator.* 