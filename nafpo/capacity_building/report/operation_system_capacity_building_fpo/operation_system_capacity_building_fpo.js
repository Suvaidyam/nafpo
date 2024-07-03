// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Operation System Capacity Building FPO"] = {
	"filters":[
		{
			"fieldname":"has_trained",
			"label": __("Has Trained"),
			"fieldtype": "Select",
			"options": ["","Yes", "No"]
		}
	]
};
