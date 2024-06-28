# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):	
	query = ""
	if filters.get("has_trained") == "Yes":
		query = f"""
		SELECT
			_fpo.fpo_name, 
			"Yes" AS has_trained,
			_fp.contact_detail_of_fpo,
			_fp.fpo_email_id
		FROM
			`tabFPO` AS _fpo
		LEFT JOIN `tabFPO Profiling` AS _fp ON _fpo.name = _fp.name_of_the_fpo
		WHERE
			_fpo.name IN (
				SELECT DISTINCT _fs.fpo
				FROM `tabCapacity` AS _cap
				INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
				INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
			);
            """
	elif filters.get("has_trained") == "No":
		query = f"""
			SELECT
				_fpo.fpo_name, 
				"No" AS has_trained,
				_fp.contact_detail_of_fpo,
				_fp.fpo_email_id
			FROM
				`tabFPO` AS _fpo
			LEFT JOIN `tabFPO Profiling` AS _fp ON _fpo.name = _fp.name_of_the_fpo
			WHERE
				_fpo.name NOT IN (
					SELECT DISTINCT _fs.fpo
					FROM `tabCapacity` AS _cap
					INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
					INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
				);
            """
	else:
		query = f"""
		SELECT
			_fpo.fpo_name, 
			"Yes" AS has_trained,
			_fp.contact_detail_of_fpo,
			_fp.fpo_email_id
		FROM
			`tabFPO` AS _fpo
		LEFT JOIN `tabFPO Profiling` AS _fp ON _fpo.name = _fp.name_of_the_fpo
		WHERE
			_fpo.name IN (
				SELECT DISTINCT _fs.fpo
				FROM `tabCapacity` AS _cap
				INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
				INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
			)
		UNION ALL

		SELECT
			_fpo.fpo_name, 
			"No" AS has_trained,
			_fp.contact_detail_of_fpo,
			_fp.fpo_email_id
		FROM
			`tabFPO` AS _fpo
		LEFT JOIN `tabFPO Profiling` AS _fp ON _fpo.name = _fp.name_of_the_fpo
		WHERE
			_fpo.name NOT IN (
				SELECT DISTINCT _fs.fpo
				FROM `tabCapacity` AS _cap
				INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
				INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
			);
		"""
	columns=[
		{
			"fieldname": "fpo_name",
			"label": "FPO Name",
			"fieldtype": "Data",
			"width": 250
		},
		{
			"fieldname": "has_trained",
			"label": "Has Trained",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "contact_detail_of_fpo",
			"label": "FPO Contact Detail",
			"fieldtype": "Data",
			"width": 250
		},
		{
			"fieldname": "fpo_email_id",
			"label": "FPO Email ID",
			"fieldtype": "Data",
			"width": 250
		}
	]
	data = frappe.db.sql(query, as_dict=True)
	return columns, data
