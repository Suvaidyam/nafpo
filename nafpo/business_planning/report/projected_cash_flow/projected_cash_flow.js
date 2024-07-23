// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Projected Cash Flow"] = {
	"filters": [


		{
			"fieldname": "fpo_name",
			"label": __("FPO Name"),
			"fieldtype": "Link",
			"options": "FPO"
		},
		{
			"fieldname": "financial_year",
			"label": __("Financial Year"),
			"fieldtype": "Link",
			"options": "Financial Year"
		}



	]
};

