# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter




def execute(filters=None):
	user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
    	mappings={'CBBO': ('fpo', 'cbbo_name'), 'IA': ('fpo', 'ia') , 'FPO': ('fpo', 'name')},
    	selected_filters=['CBBO', 'IA', 'FPO']
	)

	cond_str = f" WHERE {user_filter_conditions}" if user_filter_conditions else ""
	columns = [
		{
			"fieldname": "output_side",
			"label": "Output Side",
			"fieldtype": "Currency",
			"width": 300
		}
	]

	sql_query = f"""
	SELECT
   		COALESCE(SUM(bp.output),0) AS output_side
	FROM
    	`tabBusiness Plannings` AS bp
	INNER JOIN `tabFPO` AS fpo ON bp.fpo = fpo.name
	{cond_str}
	"""
	data = frappe.db.sql(sql_query, as_dict=1)
	return columns, data