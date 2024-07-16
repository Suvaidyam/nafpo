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
			"fieldname": "gross_output_turn_over",
			"label": "Gross Output Turn Over",
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
    SUM(os.total_selling_priceincome_rs) AS gross_output_turn_over,
    fy.financial_year_name as financial_year
FROM
    `tabBusiness Plannings` AS bp
INNER JOIN `tabOutput Side Child` AS os ON bp.name = os.parent
INNER JOIN `tabFinancial Year` AS fy ON bp.financial_year = fy.name
{cond_str}
GROUP BY
    fy.financial_year_name
	"""
	data = frappe.db.sql(sql_query, as_dict=True)
	return columns, data
