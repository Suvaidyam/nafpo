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
            "fieldname": "gender",
            "label": "",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "percentage",
            "label": "Percentage",
            "fieldtype": "Int",
            "width": 300
        },
    ]
    	
	sql_query = f"""
		SELECT 
    sub_query.gender,
    ROUND((sub_query.total_land_size_by_gender/sub_query.total_owned_land) * 100, 2) AS percentage
FROM (
    SELECT 
    gender,
        SUM(fmd.total_owned_in_hectare) AS total_land_size_by_gender,
        ROUND((SELECT SUM(total_owned_in_hectare) FROM `tabFPO member details` WHERE gender IN ('Male','Female')),2) AS total_owned_land
    FROM `tabFPO member details` AS fmd
    INNER JOIN `tabFPO` AS _fpo ON fmd.fpo = _fpo.name
    WHERE
        fmd.gender IN ('Male','Female')
		{cond_str}
    GROUP BY gender
) AS sub_query;
    """

	data = frappe.db.sql(sql_query, as_dict=True)
	return columns, data