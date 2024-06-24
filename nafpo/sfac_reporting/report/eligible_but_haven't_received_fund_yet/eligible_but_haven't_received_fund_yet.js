// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Eligible but haven't received fund yet"] = {
	"filters": [
		{
			"fieldname": "installment_",
			"fieldtype": "Autocomplete",
			"label": "Installment",
			"options": ["First Installment", "Second Installment", "Third Installment", "Fourth Installment", "Fifth Installment", "Sixth Installment"]
		}
	]
};
