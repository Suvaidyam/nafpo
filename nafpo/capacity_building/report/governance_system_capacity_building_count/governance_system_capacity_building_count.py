# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
	user_filter_conditions_top = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('fpo', 'cbbo_name'), 'State': ('fpo', 'state'), 'District': ('fpo', 'district'), 'FPO': ('fpo', 'name'), 'IA': ('subquery', 'ia')},
		selected_filters=['CBBO','State','FPO','District','IA']
	)
	user_cond_str_top = f"AND {user_filter_conditions_top}" if user_filter_conditions_top else ""
	user_filter_conditions_bottom = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('fpo', 'cbbo_name'), 'State': ('fpo', 'state'), 'District': ('fpo', 'district'), 'FPO': ('fpo', 'name'),'IA': ('_cap', 'ia')},
		selected_filters=['CBBO','State','FPO','District','IA']
	)
	user_cond_str_bottom = f"AND {user_filter_conditions_bottom}" if user_filter_conditions_bottom else ""

	columns = [
		{
            "fieldname": "trained",
            "label": "Trained",
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
	query = f"""
		SELECT COUNT(*) AS count, 'No' AS trained
		FROM (
			SELECT fpo.name
			FROM `tabFPO` AS fpo
			LEFT JOIN (
				SELECT DISTINCT _fs.fpo AS fpo, _cap.ia AS ia
				FROM `tabCapacity` AS _cap
				INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
				INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
			) AS subquery ON fpo.name = subquery.fpo
			WHERE subquery.fpo IS NULL {user_cond_str_top}
		) AS has_not_trained

		UNION ALL

		SELECT COUNT(*) AS count, 'Yes' AS trained
		FROM (
			SELECT DISTINCT fpo.name
			FROM `tabFPO` AS fpo
			LEFT JOIN `tabCapacity` AS _cap ON fpo.name = _cap.fpo
			LEFT JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
			LEFT JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
			WHERE _fs.fpo IS NOT NULL
			{user_cond_str_bottom}
		) AS has_trained;
	"""
	data = frappe.db.sql(query, as_dict=True)
	return columns, data
