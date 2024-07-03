# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
	user_filter_conditions_top = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('_fpo', 'cbbo_name'), 'State': ('_fpo', 'state'), 'District': ('_fpo', 'district'), 'FPO': ('_fpo', 'name'),"IA": ('_cap', 'ia')},
		selected_filters=['CBBO','State','FPO','District','IA']
	)
	user_cond_str_top = f"WHERE {user_filter_conditions_top}" if user_filter_conditions_top else ""
	user_filter_conditions_bottom = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('_fpo', 'cbbo_name'), 'State': ('_fpo', 'state'), 'District': ('_fpo', 'district'), 'FPO': ('_fpo', 'name'),"IA": ('trained_ceos', 'ia')},
		selected_filters=['CBBO','State','FPO','District','IA']
	)
	user_cond_str_bottom = f"AND {user_filter_conditions_bottom}" if user_filter_conditions_bottom else ""

	query = f"""
    SELECT
		COUNT(_fpo.name) AS count, 
		"Yes" AS has_trained_ceo
	FROM
		`tabFPO` AS _fpo
	WHERE
		_fpo.name IN (
			SELECT DISTINCT _fs.fpo
			FROM `tabCapacity` AS _cap
			INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
			INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name AND _fs.position_designation = "CEO"
			INNER JOIN `tabFPO` AS _fpo ON _fs.fpo = _fpo.name
			{user_cond_str_top}
		)
	UNION ALL
	
	SELECT
		COUNT(_fpo.name) AS count,
		"No" AS has_trained_ceo
	FROM
		`tabFPO` AS _fpo
	LEFT JOIN (
		SELECT DISTINCT _fs.fpo AS fpo, _cap.ia AS ia
		FROM `tabCapacity` AS _cap
		INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
		INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name AND _fs.position_designation = "CEO"
	) AS trained_ceos ON _fpo.name = trained_ceos.fpo
	WHERE
		trained_ceos.fpo IS NULL {user_cond_str_bottom};
    """
	columns = [
		{
			"fieldname": "has_trained_ceo",
			"label": "Has Trained CEO",
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
