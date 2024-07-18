# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
	user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('f', 'cbbo_name'), 'State': ('f', 'state'), 'District': ('f', 'district'), 'FPO': ('f', 'name'), 'IA': ('f', 'ia')},
		selected_filters=['CBBO','State','FPO','District','IA']
	)
	user_cond_str = f"WHERE {user_filter_conditions}" if user_filter_conditions else ""

	query = f"""
		SELECT
			CASE WHEN c.fpo IS NOT NULL THEN 'Yes' ELSE 'No' END AS trained_status,
			COUNT(DISTINCT f.name) AS count
		FROM tabFPO f
		LEFT JOIN tabCapacity c ON f.name = c.fpo
		{user_cond_str}
		GROUP BY CASE WHEN c.fpo IS NOT NULL THEN 'Yes' ELSE 'No' END;
	"""
	columns = [
		{
            "fieldname": "trained_status",
            "label": "Trained status",
            "fieldtype": "Data",
            "width": 200
        },
		{
            "fieldname": "count",
            "label": "Count",
            "fieldtype": "Int",
            "width": 200
        }
	]
	data = frappe.db.sql(query, as_dict=True)
	return columns, data
