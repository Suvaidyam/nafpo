// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Financial Year Wise Turnover"] = {
	"filters": [
		
		{
			"fieldname": "financial_year",
			"label": __("Financial Year"),
			"fieldtype": "Link",
			"options": "Financial Year"
		}
		,
		{
			"fieldname": "turnover",
			"label": __("Turnover"),
			"fieldtype": "Select",
			"options": "\nLess than 1 Lakh\n1-10 Lakhs\n10-25 Lakhs\n25-50 Lakhs\nMore than 50 Lakhs"
		},
		{
			"fieldname": "profitability",
			"label": __("Profitability"),
			"fieldtype": "Select",
			"options": "\nProfit\nLoss\nNot Filled"
		}

	]
};
