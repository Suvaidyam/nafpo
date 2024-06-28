// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Membership System Capacity Buidling"] = {
	"filters": [
		{ 
			"fieldname":"FPO_with_Training",
			"label": __("FPO with Training"),
			"fieldtype": "Select",
			"options": ["","Yes", "No"]
		}

	]
};
