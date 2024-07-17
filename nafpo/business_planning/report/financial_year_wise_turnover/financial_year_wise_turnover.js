// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Financial Year Wise Turnover"] = {
	"filters": [
		{
			"fieldname":"financial_year",
			"label": __("Financial Year"),
			"fieldtype": "Link",
			"options": "Financial Year"
		},
		{
			"fieldname":"profitability",
			"label": __("Profitability"),
			"fieldtype": "Select",
			"options": "Profit\nLoss\nBusiness Planning Not Filled"
		}
	]
};
