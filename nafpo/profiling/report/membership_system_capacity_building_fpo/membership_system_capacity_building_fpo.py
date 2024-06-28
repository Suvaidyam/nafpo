import frappe

def execute(filters=None):
	query = """
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
				INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name AND _fs.position_designation = "CEO"
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
				INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name AND _fs.position_designation = "CEO"
			);
	"""
	columns = [
		{
			"fieldname": "fpo_name",
			"label": "FPO Name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "contact_detail_of_fpo",
			"label": "Contact Detail Of FPO",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "fpo_email_id",
			"label": "FPO Email Id",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "has_trained",
			"label": "Has Trained CEO",
			"fieldtype": "Data",
			"width": 200
		}
	]
	data = frappe.db.sql(query, as_dict=1)
	return columns, data
