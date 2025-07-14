#!/usr/bin/env python3
"""
Quick Fix for ZATCA Menu Items
===============================

This script manually creates the menu items and page for the ZATCA module.

Run this script in your ERPNext environment to fix missing menu items.

Usage:
    bench --site your-site-name console
    exec(open('apps/seidit_zatca_module/fix_menu.py').read())
"""

import frappe

def fix_zatca_menu():
    """Fix ZATCA menu items and page"""
    
    print("🔧 Fixing ZATCA menu items...")
    
    # Create the page
    if not frappe.db.exists("Page", "zatca-setup-wizard"):
        frappe.get_doc({
            'doctype': 'Page',
            'name': 'zatca-setup-wizard',
            'title': 'ZATCA Setup Wizard',
            'module': 'SEIDiT ZATCA',
            'template': 'zatca-setup-wizard.html',
            'published': 1
        }).insert()
        print("✅ Created ZATCA Setup Wizard page")
    
    # Create ZATCA Setup Wizard menu item
    if not frappe.db.exists("Desktop Icon", "ZATCA Setup Wizard"):
        frappe.get_doc({
            'doctype': 'Desktop Icon',
            'module_name': 'SEIDiT ZATCA',
            'label': 'ZATCA Setup Wizard',
            'icon': 'octicon octicon-gear',
            'type': 'page',
            'link': 'zatca-setup-wizard',
            'color': '#007bff',
            'description': 'Complete ZATCA Phase 2 setup wizard',
            'category': 'Integrations'
        }).insert()
        print("✅ Created ZATCA Setup Wizard menu item")
    
    # Create ZATCA Settings menu item
    if not frappe.db.exists("Desktop Icon", "ZATCA Settings"):
        frappe.get_doc({
            'doctype': 'Desktop Icon',
            'module_name': 'SEIDiT ZATCA',
            'label': 'ZATCA Settings',
            'icon': 'octicon octicon-settings',
            'type': 'doctype',
            'link': 'ZATCA Settings',
            'color': '#28a745',
            'description': 'Configure ZATCA settings and credentials',
            'category': 'Integrations'
        }).insert()
        print("✅ Created ZATCA Settings menu item")
    
    # Create ZATCA Logs menu item
    if not frappe.db.exists("Desktop Icon", "ZATCA Logs"):
        frappe.get_doc({
            'doctype': 'Desktop Icon',
            'module_name': 'SEIDiT ZATCA',
            'label': 'ZATCA Logs',
            'icon': 'octicon octicon-list-ordered',
            'type': 'doctype',
            'link': 'ZATCA Log',
            'color': '#ffc107',
            'description': 'View ZATCA processing logs and status',
            'category': 'Integrations'
        }).insert()
        print("✅ Created ZATCA Logs menu item")
    
    # Create module def if not exists
    if not frappe.db.exists("Module Def", "SEIDiT ZATCA"):
        frappe.get_doc({
            'doctype': 'Module Def',
            'module_name': 'SEIDiT ZATCA',
            'app_name': 'seidit_zatca_module',
            'restrict_to_domain': None,
            'hidden': 0,
            'custom': 1,
            'description': 'SEIDiT ZATCA Phase 2 Module for ERPNext'
        }).insert()
        print("✅ Created SEIDiT ZATCA module")
    
    print("🎉 ZATCA menu items fixed successfully!")
    print("📋 Now you should see:")
    print("   - ZATCA Setup Wizard")
    print("   - ZATCA Settings") 
    print("   - ZATCA Logs")
    print("   in your ERPNext menu under 'Integrations' category")

# Run the fix
if __name__ == "__main__":
    fix_zatca_menu() 