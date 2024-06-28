# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	query = """ SELECT
		f.fpo_name AS FPO_Name,
		CASE 
			WHEN COUNT(DISTINCT CASE WHEN c.fpo IS NOT NULL THEN f.name END) > 0 THEN 'Yes'
			ELSE 'No'
		END AS FPO_with_Training,
		
		p.fpo_email_id AS FPO_email_id,
		p.contact_detail_of_fpo AS FPO_Contact_Detail
	FROM `tabFPO` f
	LEFT JOIN `tabCapacity` c ON f.name = c.fpo
	LEFT JOIN `tabFPO Profiling` p ON f.name = p.name_of_the_fpo
	GROUP BY f.fpo_name, p.fpo_email_id, p.contact_detail_of_fpo;
	"""
	columns = [
		{
			"label": "FPO Name",
			"fieldname": "FPO_Name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": "FPO with Training",
			"fieldname": "FPO_with_Training",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": "FPO Email ID",
			"fieldname": "FPO_email_id",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": "FPO Contact Detail",
			"fieldname": "FPO_Contact_Detail",
			"fieldtype": "Data",
			"width": 200
		}
	]
	data = frappe.db.sql(query, as_dict=True)
	return columns, data

