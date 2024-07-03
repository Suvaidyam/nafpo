# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
	user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('_fpo', 'cbbo_name'), 'State': ('_fpo', 'state'), 'District': ('_fpo', 'district'), 'FPO': ('_bk', 'fpo_name'), 'IA': ('_bk', 'ia')},
		selected_filters=['CBBO','State','FPO','District','IA']
	)
	user_cond_str = f"AND {user_filter_conditions}" if user_filter_conditions else ""

	if filters.get('attended_training') == 'Yes':
		query = f"""
		SELECT
			"Yes" AS attended_training,
			_bk.mobile_number,
			_fpo.fpo_name,
			_bk.name1 AS bod_name
		FROM
			`tabBOD KYC` AS _bk
		INNER JOIN `tabFPO` AS _fpo ON _bk.fpo_name = _fpo.name
		WHERE
			_bk.name IN (SELECT
				_bkc.bod_kyc
			FROM
				`tabBOD KYC Child` AS _bkc
			WHERE
				_bkc.parenttype = 'Capacity')
		{user_cond_str}
		"""
	elif filters.get('attended_training') == 'No':
		query = f"""
		SELECT
			"No" AS attended_training,
			_bk.mobile_number,
			_fpo.fpo_name,
			_bk.name1 AS bod_name
		FROM
			`tabBOD KYC` AS _bk
		INNER JOIN `tabFPO` AS _fpo ON _bk.fpo_name = _fpo.name
		WHERE
			_bk.name NOT IN (SELECT
				_bkc.bod_kyc
			FROM
				`tabBOD KYC Child` AS _bkc
			WHERE
				_bkc.parenttype = 'Capacity')
		{user_cond_str}
		"""
	else:
		query = f"""
		SELECT
			"Yes" AS attended_training,
			_bk.mobile_number,
			_fpo.fpo_name,
			_bk.name1 AS bod_name
		FROM
			`tabBOD KYC` AS _bk
		INNER JOIN `tabFPO` AS _fpo ON _bk.fpo_name = _fpo.name
		WHERE
			_bk.name IN (SELECT
				_bkc.bod_kyc
			FROM
				`tabBOD KYC Child` AS _bkc
			WHERE
				_bkc.parenttype = 'Capacity')
		{user_cond_str}
		UNION ALL

		SELECT
			"No" AS attended_training,
			_bk.mobile_number,
			_fpo.fpo_name,
			_bk.name1 AS bod_name
		FROM
			`tabBOD KYC` AS _bk
		INNER JOIN `tabFPO` AS _fpo ON _bk.fpo_name = _fpo.name
		WHERE
			_bk.name NOT IN (SELECT
				_bkc.bod_kyc
			FROM
				`tabBOD KYC Child` AS _bkc
			WHERE
				_bkc.parenttype = 'Capacity')
		{user_cond_str}
		"""
	columns=[
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
			"fieldname": "fpo_name",
			"label": "FPO Name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "bod_name",
			"label": "BOD Name",
			"fieldtype": "Data",
			"width": 200
		}
	]
	data = frappe.db.sql(query, as_dict=1)
	return columns, data
