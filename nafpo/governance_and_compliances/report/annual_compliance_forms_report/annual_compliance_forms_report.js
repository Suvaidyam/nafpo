// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Annual Compliance Forms Report"] = {
	"filters": [
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Autocomplete",
			"options": ["Pending", "Completed Before Due Date", "Completed After Due Date"],
		}
	]
};
