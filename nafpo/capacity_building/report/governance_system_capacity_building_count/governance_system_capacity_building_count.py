# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
	# user_filter_conditions_top = ReportFilter.rport_filter_by_user_permissions(
	# 	mappings={'CBBO': ('fpo', 'cbbo_name'), 'State': ('fpo', 'state'), 'District': ('fpo', 'district'), 'FPO': ('fpo', 'name'), 'IA': ('fpo', 'ia')},
	# 	selected_filters=['CBBO','State','FPO','District','IA']
	# )
	# user_cond_str = f"AND {user_filter_conditions_top}" if user_filter_conditions_top else ""

	# columns = [
	# 	{
    #         "fieldname": "trained",
    #         "label": "Trained",
    #         "fieldtype": "Data",
    #         "width": 200
    #     },
	# 	{
    #         "fieldname": "count",
    #         "label": "Count",
    #         "fieldtype": "Int",
    #         "width": 200
    #     }
	# ]
	# query = f"""
	# 	SELECT COUNT(*) AS count, 'No' AS trained
	# 	FROM (
	# 		SELECT fpo.name
	# 		FROM `tabFPO` AS fpo
	# 		LEFT JOIN (
	# 			SELECT DISTINCT _fs.fpo AS fpo, _cap.ia AS ia
	# 			FROM `tabCapacity` AS _cap
	# 			INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
	# 			INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
	# 		) AS subquery ON fpo.name = subquery.fpo
	# 		WHERE subquery.fpo IS NULL {user_cond_str}
	# 	) AS has_not_trained

	# 	UNION ALL

	# 	SELECT COUNT(*) AS count, 'Yes' AS trained
	# 	FROM (
	# 		SELECT DISTINCT fpo.name
	# 		FROM `tabFPO` AS fpo
	# 		LEFT JOIN `tabCapacity` AS _cap ON fpo.name = _cap.fpo AND _cap.name IN (SELECT name FROM `tabCapacity` WHERE category = 'Governance System (BOD)')
	# 		LEFT JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
	# 		LEFT JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
	# 		WHERE _fs.fpo IS NOT NULL
	# 		{user_cond_str}
	# 	) AS has_trained;
	# """


	user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('f', 'cbbo_name'), 'State': ('f', 'state'), 'District': ('f', 'district'), 'FPO': ('f', 'name'), 'IA': ('f', 'ia')},
		selected_filters=['CBBO','State','FPO','District','IA']
	)
	user_cond_str = f"WHERE {user_filter_conditions}" if user_filter_conditions else ""

	query = f"""
		SELECT
			all_statuses.trained_status,
			COALESCE(subquery.count, 0) AS count
		FROM (
			SELECT
				CASE WHEN c.fpo IS NOT NULL THEN 'Yes' ELSE 'No' END AS trained_status,
				COUNT(DISTINCT f.name) AS count
			FROM tabFPO f
			LEFT JOIN tabCapacity c ON f.name = c.fpo AND c.name IN (SELECT name FROM `tabCapacity` WHERE category = 'Governance System (BOD)')
			{user_cond_str}
			GROUP BY CASE WHEN c.fpo IS NOT NULL THEN 'Yes' ELSE 'No' END
		) AS subquery
		RIGHT JOIN (
			SELECT 'Yes' AS trained_status
			UNION ALL
			SELECT 'No' AS trained_status
		) AS all_statuses ON subquery.trained_status = all_statuses.trained_status
		ORDER BY all_statuses.trained_status ASC;
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
