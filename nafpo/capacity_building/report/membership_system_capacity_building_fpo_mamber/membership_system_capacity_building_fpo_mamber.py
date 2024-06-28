# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    query = """
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
	"""
    columns = [
        {
			"fieldname": "attended_training",
			"label": "Attended Training",
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
			"fieldname": "fpo_name",
			"label": "FPO Name",
			"fieldtype": "Data",
			"width": 200
		}
	]
    data = frappe.db.sql(query, as_dict=True)
    return columns, data
