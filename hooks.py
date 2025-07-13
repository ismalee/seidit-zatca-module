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
# app_include_css = "/assets/seidit_zatca_module/css/seidit_zatca_module.css"

# Includes in <head>
# app_include_js = "/assets/seidit_zatca_module/js/seidit_zatca_module.js"

# Home Pages
# application_ home_controller and corresponding route has no index() function. But has an APP_NAME_home_controller file that has been rendered, instead

# page_js = {"page" : "public/js/file.js"}

# Docs
# doc = [
# 	{ "type" : "title", "label" : "ZATCA Settings" },
# 	{ "type" : "doctype", "name" : "ZATCA Settings" },
# ]

# Installation
# on_install = "seidit_zatca_module.install.install"

# Uninstallation
# on_uninstall = "seidit_zatca_module.uninstall.uninstall"

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
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

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

# Document Events
# doc_events = {
# 	"Sales Invoice": {
# 		"on_submit": "seidit_zatca_module.zatca_phase2_module.submit_to_zatca",
# 		"on_cancel": "seidit_zatca_module.zatca_phase2_module.cancel_zatca_invoice"
# 	}
# } 