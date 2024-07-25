// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.query_reports["Projected Cash Flow"] = {
	"filters": [


		{
			"fieldname": "fpo_name",
			"label": __("FPO"),
			"fieldtype": "Link",
			"options": "FPO"
		},
		{
            "fieldname": "financial_year",
            "label": __("Financial Year"),
            "fieldtype": "MultiSelectList",
            "get_data": function(txt) {
                return frappe.db.get_link_options('Financial Year', txt);
            }
        }



	]
};

