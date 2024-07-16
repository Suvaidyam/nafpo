# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter


def execute(filters=None):
	user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
		mappings={'FPO': ('bp', 'fpo')},
		selected_filters=['FPO']
	)
	cond_str = f" WHERE {user_filter_conditions}" if user_filter_conditions else ""
	columns = [
		{
			"fieldname": "gross_input_turn_over",
			"label": "Gross Input Turn Over",
			"fieldtype": "Currency",
			"width": 300
		},
		{
			"fieldname": "financial_year",
			"label": "Financial Year",
			"fieldtype": "Data",
			"width": 300
		}
	]
	sql_query = f"""
	SELECT
    SUM(ins.total_selling_priceincome_rs) AS gross_input_turn_over,
    fy.financial_year_name as financial_year
FROM
    `tabBusiness Plannings` AS bp
INNER JOIN `tabInput Side Child` AS ins ON bp.name = ins.parent
INNER JOIN `tabFinancial Year` AS fy ON bp.financial_year = fy.name
{cond_str}
GROUP BY
    fy.financial_year_name
	"""
	data = frappe.db.sql(sql_query, as_dict=True)
	return columns, data

