# -*- coding: utf-8 -*-
app_name = "seidit_zatca_module"
app_title = "SEIDiT ZATCA Module"
app_publisher = "SEIDiT"
app_description = "SEIDiT ZATCA Phase 2 Module for ERPNext"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "support@seidit.com"
app_license = "Proprietary"

# Includes in <head>
app_include_css = "/assets/seidit_zatca_module/css/zatca_wizard.css"

# Includes in <head>
app_include_js = "/assets/seidit_zatca_module/js/zatca_wizard.js"

# Home Pages
# application_ home_controller and corresponding route has no index() function. But has an APP_NAME_home_controller file that has been rendered, instead

# page_js = {"page" : "public/js/file.js"}

# Docs
doc = [
	{ "type" : "title", "label" : "ZATCA Settings" },
	{ "type" : "doctype", "name" : "ZATCA Settings" },
	{ "type" : "title", "label" : "ZATCA Setup Wizard" },
	{ "type" : "page", "name" : "zatca-setup-wizard" },
	{ "type" : "title", "label" : "ZATCA Logs" },
	{ "type" : "doctype", "name" : "ZATCA Log" },
]

# Installation
on_install = "seidit_zatca_module.install.install"

# Uninstallation
on_uninstall = "seidit_zatca_module.install.uninstall"

# Desk Notifications
# See frappe.core.notifications.get_notification_config

# notification_config = "seidit_zatca_module.notifications.get_notification_config"

# Permissions
# Permissions evaluated in function called in "after_migrate" in hooks.py

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# Events are coded in the doctype class. These are executed with the 'on_' prefix
doc_events = {
	"Sales Invoice": {
		"on_submit": "seidit_zatca_module.zatca_core.on_sales_invoice_submit",
		"on_cancel": "seidit_zatca_module.zatca_core.on_sales_invoice_cancel"
	}
}

# Scheduled Tasks
# scheduler_events = {
# 	"all": [
# 		"seidit_zatca_module.tasks.all"
# 	],
# 	"daily": [
# 		"seidit_zatca_module.tasks.daily"
# 	],
# 	"hourly": [
# 		"seidit_zatca_module.tasks.hourly"
# 	],
# 	"weekly": [
# 		"seidit_zatca_module.tasks.weekly"
# 	]
# 	"monthly": [
# 		"seidit_zatca_module.tasks.monthly"
# 	]
# }

# Testing
# before_tests = "seidit_zatca_module.install.before_tests"

# Overriding Methods
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "seidit_zatca_module.event.get_events"
# }

# Overriding JS Methods
# override_js = "assets/js/seidit_zatca_module.min.js"

required_apps = [
	"erpnext"
]

# Add to apps screen
add_to_apps_screen = [
	{
		"name": "seidit_zatca_module",
		"description": "SEIDiT ZATCA Phase 2 Module for ERPNext",
		"icon": "octicon octicon-file-directory",
		"color": "blue",
		"category": "Integrations"
	}
]

# Add menu items automatically
def after_migrate():
    """Create menu items after migration"""
    import frappe
    
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