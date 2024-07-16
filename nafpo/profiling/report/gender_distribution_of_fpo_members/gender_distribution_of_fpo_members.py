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
			"fieldname":"gender",
			"label":"Gender",
			"fieldtype":"Data",
			"width":200
		},
		{
			"fieldname":"count",
			"label":"Count",
			"fieldtype":"Int",
			"width":200
		}
	]
	
	sql_query = f"""
SELECT
    g.gender AS gender,
    COALESCE(COUNT(fmd.name), 0) AS count
FROM
    (SELECT 'Male' AS gender
     UNION ALL
     SELECT 'Female') AS g
LEFT JOIN `tabFPO member details` fmd ON fmd.gender = g.gender
LEFT JOIN `tabFPO` AS _fpo ON fmd.fpo = _fpo.name
WHERE fmd.gender IN ('Male','Female')
	{cond_str}
GROUP BY
    g.gender
	"""
	data = frappe.db.sql(sql_query, as_dict=True)
	return columns, data
