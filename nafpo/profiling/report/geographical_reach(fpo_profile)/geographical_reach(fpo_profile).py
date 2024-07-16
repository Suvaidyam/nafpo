# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
	user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('_fpo', 'cbbo_name'), 'IA': ('_fpo', 'ia'), 'FPO': ('_fpo', 'name')},
		selected_filters=['CBBO', 'IA', 'FPO'],
	)
	cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""

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
		}

	]

	query = f"""
		SELECT
			COUNT(DISTINCT CASE WHEN _fp.state_name != '' THEN _fp.state_name ELSE NULL END) AS state_count,
			COUNT(DISTINCT CASE WHEN _fp.district_name != '' THEN _fp.district_name ELSE NULL END) AS district_count,
			COUNT(DISTINCT _bc.block) AS block_count
		FROM
			`tabFPO Profiling` AS _fp
		INNER JOIN `tabBlock Child` AS _bc ON _fp.name = _bc.parent
		INNER JOIN `tabFPO` AS _fpo ON _fp.name_of_the_fpo = _fpo.name
		WHERE
			_bc.parenttype = 'FPO Profiling' {cond_str}
		"""
	data = frappe.db.sql(query, as_dict=True)
	return columns,data