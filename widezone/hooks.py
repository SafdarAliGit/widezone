from . import __version__ as app_version

app_name = "widezone"
app_title = "Lucrum WideZone"
app_publisher = "LucrumERP"
app_description = "LucrumERP Customization for WideZone"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@lucrumerp.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/widezone/css/widezone.css"
# app_include_js = "/assets/widezone/js/widezone.js"

# include js, css files in header of web template
# web_include_css = "/assets/widezone/css/widezone.css"
# web_include_js = "/assets/widezone/js/widezone.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "widezone/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}

# override_doctype_class = {
# 	"Outward Gate Pass": "lucrum_gate_pass.overrides.outward_gate_pass_override.OutwardGatePass"
# }



doctype_js = {
	"Material Request" : "public/material_request_custom.js",
	"Quotation" : "public/quotation_custom.js",
	"Inward Gate Pass" : "public/inward_gatepass_custom.js",
	"Outward Gate Pass" : "public/outward_gatepass_custom.js",
	"Stock Entry":"public/stock_entry_custom.js",
	"Purchase Order":"public/purchase_order_custom.js",
	"Sales Order":"public/js/sales_order_custom.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "widezone.install.before_install"
# after_install = "widezone.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "widezone.uninstall.before_uninstall"
# after_uninstall = "widezone.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "widezone.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
	"*": {
		"before_naming": "widezone.custom.naming_custom.before_naming"
	},
	"Quotation": {
		"validate": "lucrum_bari.custom.quotation_custom.validate"
	},
	"Item Attribute": {
		"validate": "widezone.custom.item_attribute_custom.validate"
	},
	"Inward Gate Pass": {
		"validate": "widezone.custom.inward_gatepass_custom.validate"
	},
	"Purchase Order": {
		"validate": "widezone.custom.purchase_order_custom.validate",
		"on_submit": "widezone.custom.purchase_order_custom.submit"
	},
	"Purchase Receipt": {
		"validate": "widezone.custom.purchase_receipt_custom.validate"
	},
	"Employee":{
		"before_naming":"widezone.custom.employee_custom.before_naming"
	},
	"Sales Order":{
		"validate":"widezone.custom.sales_order_custom.validate"
	},
	"Material Request":{
		"validate":"widezone.custom.material_request_custom.validate"
	},
	"Outward Gate Pass":{
		"validate":"widezone.custom.outward_gatepass_custom.validate",
		"on_submit":"widezone.custom.outward_gatepass_custom.submit",
		}
	
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"widezone.tasks.all"
# 	],
# 	"daily": [
# 		"widezone.tasks.daily"
# 	],
# 	"hourly": [
# 		"widezone.tasks.hourly"
# 	],
# 	"weekly": [
# 		"widezone.tasks.weekly"
# 	]
# 	"monthly": [
# 		"widezone.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "widezone.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "widezone.event.get_events"
# }

override_whitelisted_methods = {
	"lucrum.controllers.item_variant.create_variant": "widezone.custom.item_variant_custom.create_variant_custom"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other frappe apps
# override_doctype_dashboards = {
# 	"Task": "widezone.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"widezone.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []

required_apps = ["erpnext"]
