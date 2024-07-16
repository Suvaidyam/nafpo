# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
	user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
		mappings={'FPO': ('no_alias', 'fpo')},
		selected_filters=['FPO']
	)
	cond_str = f" WHERE {user_filter_conditions}" if user_filter_conditions else ""
	columns = [
		{
			"fieldname": "fixed_capital_cost",
			"label": "Fixed Capital Cost",
			"fieldtype": "Currency",
			"width": 200
		}

	]
	
	sq1 = f"""
	SELECT
		SUM(total_value) AS fixed_capital_cost
	FROM
		`tabFPO Fixed Capital`
	{cond_str}
	"""
	data = frappe.db.sql(sq1, as_dict=1)
	return columns, data



