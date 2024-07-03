# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('_fpo', 'cbbo_name'), 'State': ('_fpo', 'state'), 'District': ('_fpo', 'district'), 'FPO': ('_fpo', 'name'), 'IA': ('_fmd', 'ia')},
        selected_filters=['CBBO','State','FPO','District','IA']
    )
    user_cond_str = f"AND {user_filter_conditions}" if user_filter_conditions else ""
    
    if filters.get("attended_training") == "Yes":
        query = f"""
            SELECT
                "Yes" AS attended_training,
                _fmd.mobile_number,
                _fmd.member_name,
                _fpo.fpo_name
            FROM
                `tabFPO member details` AS _fmd
            INNER JOIN `tabFPO` AS _fpo ON _fmd.fpo = _fpo.name
            WHERE
                _fmd.name IN (SELECT
                    _fmdc.fpo_member
                FROM
                    `tabFPO member details Child` AS _fmdc
                WHERE
                    _fmdc.parenttype = 'Capacity')
                {user_cond_str}
        """
    elif filters.get("attended_training") == "No":
        query = f"""
            SELECT
                "No" AS attended_training,
                _fmd.mobile_number,
                _fmd.member_name,
                _fpo.fpo_name
            FROM
                `tabFPO member details` AS _fmd
            INNER JOIN `tabFPO` AS _fpo ON _fmd.fpo = _fpo.name
            WHERE
                _fmd.name NOT IN (SELECT
                    _fmdc.fpo_member
                FROM
                    `tabFPO member details Child` AS _fmdc
                WHERE
                    _fmdc.parenttype = 'Capacity')
                {user_cond_str}
        """
    else:
        query = f"""
            SELECT
                "Yes" AS attended_training,
                _fmd.mobile_number,
                _fmd.member_name,
                _fpo.fpo_name
            FROM
                `tabFPO member details` AS _fmd
            INNER JOIN `tabFPO` AS _fpo ON _fmd.fpo = _fpo.name
            WHERE
                _fmd.name IN (SELECT
                    _fmdc.fpo_member
                FROM
                    `tabFPO member details Child` AS _fmdc
                WHERE
                    _fmdc.parenttype = 'Capacity')
                {user_cond_str}
            UNION ALL
            
            SELECT
                "No" AS attended_training,
                _fmd.mobile_number,
                _fmd.member_name,
                _fpo.fpo_name
            FROM
                `tabFPO member details` AS _fmd
            INNER JOIN `tabFPO` AS _fpo ON _fmd.fpo = _fpo.name
            WHERE
                _fmd.name NOT IN (SELECT
                    _fmdc.fpo_member
                FROM
                    `tabFPO member details Child` AS _fmdc
                WHERE
                    _fmdc.parenttype = 'Capacity')
                {user_cond_str}
        """
    columns = [
        {
			"fieldname": "fpo_name",
			"label": "FPO Name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "mobile_number",
			"label": "Mobile Number",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "member_name",
			"label": "Member Name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "attended_training",
			"label": "Attended Training",
			"fieldtype": "Data",
			"width": 200
		}
	]
    data = frappe.db.sql(query, as_dict=True)
    return columns, data
