# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
	user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('_fpo', 'cbbo_name'), 'IA': ('_fpo', 'ia'), 'FPO': ('_fpo', 'name')},
		selected_filters=['CBBO', 'IA', 'FPO'],
	)
	cond_str = f" WHERE {user_filter_conditions}" if user_filter_conditions else ""

	columns = [
		{
			"fieldname": "state_count",
			"label": "State Count",
			"fieldtype": "Int",
			"width": 200
		},
		{
			"fieldname": "district_count",
			"label": "District Count",
			"fieldtype": "Int",
			"width": 200
		},
		{
			"fieldname": "block_count",
			"label": "Block Count",
			"fieldtype": "Int",
			"width": 200
		},
		{
			"fieldname": "grampanchayat_count",
			"label": "Grampanchayat Count",
			"fieldtype": "Int",
			"width": 200
		},
		{
			"fieldname": "village_count",
			"label": "Village Count",
			"fieldtype": "Int",
			"width": 200
		}
	]

	query = f"""
		SELECT
			COUNT(DISTINCT CASE WHEN fmd.state_name != '' THEN fmd.state_name ELSE NULL END) AS state_count,
			COUNT(DISTINCT CASE WHEN fmd.district_name != '' THEN fmd.district_name ELSE NULL END) AS district_count,
			COUNT(DISTINCT CASE WHEN fmd.block_name != '' THEN fmd.block_name ELSE NULL END) AS block_count,
			COUNT(DISTINCT CASE WHEN fmd.grampanchayat_name != '' THEN fmd.grampanchayat_name ELSE NULL END) AS grampanchayat_count,
			COUNT(DISTINCT CASE WHEN fmd.village_name != '' THEN fmd.village_name ELSE NULL END) AS village_count
		FROM
			`tabFPO member details` AS fmd
		INNER JOIN `tabFPO` AS _fpo ON fmd.fpo = _fpo.name
		{cond_str}
		"""
	data = frappe.db.sql(query, as_dict=True)
	return columns,data