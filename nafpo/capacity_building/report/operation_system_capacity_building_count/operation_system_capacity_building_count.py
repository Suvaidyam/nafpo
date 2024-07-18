# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
	user_filter_conditions_bottom = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('fpo', 'cbbo_name'), 'State': ('fpo', 'state'), 'District': ('fpo', 'district'), 'FPO': ('fpo', 'name'),"IA": ('fpo', 'ia')},
		selected_filters=['CBBO','State','FPO','District',"IA"]
	)
	user_cond_str = f"AND {user_filter_conditions_bottom}" if user_filter_conditions_bottom else ""

	query = f"""
	SELECT 
		(SELECT COUNT(*)
		FROM (
			SELECT
				DISTINCT fpo.name
			FROM
				`tabCapacity` AS _cap
			INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
			INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
			INNER JOIN `tabFPO` AS fpo ON _fs.fpo = fpo.name
			{user_cond_str}
		) AS has_trained) AS count, 'Yes' AS trained

	UNION ALL

	SELECT COUNT(fpo.name) AS count, 'No' AS trained
	FROM `tabFPO` AS fpo
	LEFT JOIN (
		SELECT DISTINCT _fs.fpo AS fpo, _cap.ia AS ia
		FROM `tabCapacity` AS _cap
		INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
		INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
	) AS trained_fpos ON fpo.name = trained_fpos.fpo
	WHERE trained_fpos.fpo IS NULL {user_cond_str};
    """
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
	data = frappe.db.sql(query, as_dict=True)
	return columns, data
