app_name = "nafpo"
app_title = "Nafpo"
app_publisher = "dhwaniris"
app_description = "a dhwaniris project on frappe"
app_email = "amresh.yadav@dhwaniris.com"
app_license = "mit"
# required_apps = []

fixtures = [
    "Role",
    "Role Profile",
    "Financial Year",
    "IA",
    "CBBO",
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/nafpo/css/nafpo.css"
# app_include_js = "/assets/nafpo/js/nafpo.js"

# include js, css files in header of web template
# web_include_css = "/assets/nafpo/css/nafpo.css"
# web_include_js = "/assets/nafpo/js/nafpo.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "nafpo/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "District" : [
        "public/js/utils/utils.js"
    ],
    "Block" : [
        "public/js/utils/utils.js"
    ],
    "Grampanchayat" : [
        "public/js/utils/utils.js"
    ],
    "Village" : [
        "public/js/utils/utils.js"
    ],
    "CBBO" : [
        "public/js/utils/utils.js"
    ],
    "FPO" : [
        "public/js/utils/utils.js"
    ],
    "Crop Type" : [
        "public/js/utils/utils.js"
    ],
    "Crop Name" : [
        "public/js/utils/utils.js"
    ],
    "BOD KYC" : [
        "public/js/utils/utils.js"
    ],
    "FPO Profiling" : [
        "public/js/utils/utils.js"
    ],
    "Producer Groups" : [
        "public/js/utils/utils.js"
    ],
    "FPO member details" : [
        "public/js/utils/utils.js"
    ],
    "CBBO Management" : [
        "public/js/utils/utils.js"
    ],
    "First Installment Fpos" : [
        "public/js/utils/utils.js"
    ],
    "Compliance and Frequency" : [
        "public/js/utils/utils.js"
    ],
    "Compliance Frequency Mapper" : [
        "public/js/utils/utils.js"
    ],
    "Email Directory" : [
        "public/js/utils/utils.js"
    ],
    "Training Material" : [
        "public/js/utils/utils.js"
    ],
    "Crop POP" : [
        "public/js/utils/utils.js"
    ],
    "Research Study Surveys" : [
        "public/js/utils/utils.js"
    ],
    "Success Stories" : [
        "public/js/utils/utils.js"
    ],
    "Other Format" : [
        "public/js/utils/utils.js"
    ],
    "Nafpo User" : [
        "public/js/utils/utils.js"
    ],
    "Financial Year" : [
        "public/js/utils/utils.js"
    ],
    "Capacity" : [
        "public/js/utils/utils.js"
    ],
    "State" : [
        "public/js/utils/utils.js"
    ],
    "One Time Organization Registration Forms" : [
        "public/js/utils/utils.js"
    ],
    "Annual Compliance Forms" : [
        "public/js/utils/utils.js"
    ],
    "Board of Directors Meeting Forms" : [
        "public/js/utils/utils.js"
    ],
    "First Installment FPOs" : [
        "public/js/utils/utils.js"
    ],
    "Second Installment FPOs" : [
        "public/js/utils/utils.js"
    ],
    "Third Installment FPOs" : [
        "public/js/utils/utils.js"
    ],
    "Fourth Installment FPOs" : [
        "public/js/utils/utils.js"
    ],
    "Fifth Installment FPOs" : [
        "public/js/utils/utils.js"
    ],
    "Six Installment Fpo" : [
        "public/js/utils/utils.js"
    ],
}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "nafpo/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "nafpo.utils.jinja_methods",
# 	"filters": "nafpo.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "nafpo.install.before_install"
# after_install = "nafpo.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "nafpo.uninstall.before_uninstall"
# after_uninstall = "nafpo.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "nafpo.utils.before_app_install"
# after_app_install = "nafpo.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "nafpo.utils.before_app_uninstall"
# after_app_uninstall = "nafpo.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "nafpo.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
}
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
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"nafpo.tasks.all"
# 	],
# 	"daily": [
# 		"nafpo.tasks.daily"
# 	],
# 	"hourly": [
# 		"nafpo.tasks.hourly"
# 	],
# 	"weekly": [
# 		"nafpo.tasks.weekly"
# 	],
# 	"monthly": [
# 		"nafpo.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "nafpo.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "nafpo.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "nafpo.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

ignore_links_on_delete = ["Route History"]

# Request Events
# ----------------
# before_request = ["nafpo.utils.before_request"]
# after_request = ["nafpo.utils.after_request"]

# Job Events
# ----------
# before_job = ["nafpo.utils.before_job"]
# after_job = ["nafpo.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"nafpo.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

