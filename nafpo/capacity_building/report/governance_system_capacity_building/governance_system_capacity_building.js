// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Governance System Capacity Building"] = {
	"filters": [
		{ 
			"fieldname":"Has_Trained_Bod",
			"label": __("Has Trained BOD"),
			"fieldtype": "Select",
			"options": ["","Yes", "No"]
		}
	]
};
