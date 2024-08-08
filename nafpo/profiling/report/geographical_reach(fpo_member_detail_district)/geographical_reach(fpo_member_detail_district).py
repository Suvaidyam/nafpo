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
			"fieldname": "district",
			"label": "District",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "hidden_count",
			"label": "Hidden Count",
			"fieldtype": "Data",
			"width": 200,
			"hidden": 1
		},

	]

	query = f"""
		SELECT
			DISTINCT dt.name,
			dt.district_name AS district,
			1 AS hidden_count
		FROM
			`tabFPO member details` AS fmd
		INNER JOIN `tabDistrict` AS dt ON fmd.district_name = dt.name
		INNER JOIN `tabFPO` AS _fpo ON fmd.fpo = _fpo.name
		{cond_str}
		"""
	data = frappe.db.sql(query, as_dict=True)
	return columns,data