// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["AGM - Once in a year fpo need to organize AGM and pass the Audit report and other agenda Report"] = {
	"filters": [
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Autocomplete",
			"options": ["Pending", "Completed Before Due Date", "Completed After Due Date"],
			"default": "Completed Before Due Date"
		}
	]
};
