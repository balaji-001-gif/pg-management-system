app_name = "pg_management"
app_title = "PG Management"
app_publisher = "PG Management"
app_description = "PG (Paying Guest) Management System for ERPNext"
app_email = "info@pgmanagement.com"
app_license = "MIT"
app_version = "1.0.0"

# Required apps
required_apps = ["frappe"]

# Fixtures — export these DocTypes with the app
fixtures = [
	{
		"dt": "Number Card",
		"filters": [["module", "=", "PG Management"]],
	},
]

# Setup after install
after_install = "pg_management.pg_management.install.after_install"
after_migrate = "pg_management.pg_management.install.after_install"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/pg_management/css/pg_management.css"
# app_include_js = "/assets/pg_management/js/pg_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/pg_management/css/pg_management.css"
# web_include_js = "/assets/pg_management/js/pg_management.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# Add methods and filters for jinja templates
# jinja = {
# 	"methods": "pg_management.utils.jinja_methods",
# 	"filters": "pg_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "pg_management.install.before_install"
# after_install = "pg_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "pg_management.uninstall.before_uninstall"
# after_uninstall = "pg_management.uninstall.after_uninstall"

# Desk Notifications
# ------------------

# See frappe.core.notifications.get_notification_config

# notification_config = "pg_management.notifications.get_notification_config"

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
# 		"on_trash": "method",
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"pg_management.tasks.all"
# 	],
# }

# Testing
# -------

# before_tests = "pg_management.install.before_tests"

# Overriding Methods
# ------------------------------

# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pg_management.event.get_events"
# }

# Each overriding function accepts a `data` argument;
# generated from the default print format

# override_doctype_dashboards = {
# 	"Task": "pg_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------

# before_request = ["pg_management.utils.before_request"]
# after_request = ["pg_management.utils.after_request"]

# Job Events
# ----------

# before_job = ["pg_management.utils.before_job"]
# after_job = ["pg_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"pg_management.auth.validate"
# ]
