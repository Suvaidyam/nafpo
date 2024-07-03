// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Governance System Capacity Building FPO BOD"] = {
	"filters": [
		{ 
			"fieldname":"attended_training",
			"label": __("Attended training"),
			"fieldtype": "Select",
			"options": ["","Yes", "No"]
		}
	]
};
