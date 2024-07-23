frappe.query_reports["Form INC-20A – BUSINESS COMMENCEMENT- MCA Report"] = {
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
