// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Membership System Capacity Building FPO Mamber"] = {
	"filters": [
		{ 
			"fieldname":"attended_training",
			"label": __("Attended training"),
			"fieldtype": "Select",
			"options": ["","Yes", "No"]
		}
	]
};
