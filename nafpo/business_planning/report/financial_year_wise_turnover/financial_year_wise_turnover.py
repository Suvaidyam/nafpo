# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from nafpo.utils.rport_filter import ReportFilter
import datetime

def execute(filters=None):
	user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
		mappings={'CBBO': ('_fpo', 'cbbo_name'),'IA': ('_fpo', 'ia'),'FPO': ('_fpo', 'name')},
		selected_filters=['FPO','CBBO','IA']
	)
	cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
	financial_year_cond = ''
	profitability_cond = ''
	turnover_cond = ''
	current_year = datetime.datetime.now().year
	financial_year = filters.get('financial_year') or frappe.get_list('Financial Year', filters={'start_date': ['between', [f'{current_year}-01-01', f'{current_year}-12-31']]},pluck='name')[0] or None
	profitability = filters.get('profitability') or None
	turnover_range = filters.get('turnover') or None
	if financial_year is not None:
		financial_year_cond = f" AND bp.financial_year = '{financial_year}'"
	if profitability is not None:
		if profitability == 'Profit':
			profitability_cond = f"AND bp.total_sales > 0"
		elif profitability == 'Loss':
			profitability_cond = f"AND bp.total_sales < 0"
		elif profitability == 'Not Filled':
			profitability_cond = f"AND bp.fpo IS NULL"
			financial_year_cond = ""
	if turnover_range is not None:
		if turnover_range == 'No Sales Data':
			turnover_cond = f" AND bp.total_sales IS NULL"
		elif turnover_range == 'Less than 1 Lakh':
			turnover_cond = f" AND bp.total_sales < 100000"
		elif turnover_range == '1-10 Lakhs':
			turnover_cond = f" AND bp.total_sales >= 100000 AND bp.total_sales < 1000000"
		elif turnover_range == '10-25 Lakhs':
			turnover_cond = f" AND bp.total_sales >= 1000000 AND bp.total_sales < 2500000"
		elif turnover_range == '25-50 Lakhs':
			turnover_cond = f" AND bp.total_sales >= 2500000 AND bp.total_sales < 5000000"
		else:
			turnover_cond = f" AND bp.total_sales >= 5000000"
	

	query = f"""
		SELECT
			bp.total_sales AS turnover,
			_fpo.fpo_name AS fpo_name,
			_fy.financial_year_name AS financial_year,
			_fp.contact_detail_of_fpo AS contact_detail_of_fpo,
			_fp.fpo_email_id AS fpo_email_id,
			CASE
				WHEN bp.total_sales IS NULL THEN 'No Sales Data'
				WHEN bp.total_sales < 100000 THEN 'Less than 1 Lakh'
				WHEN bp.total_sales >= 100000 AND bp.total_sales < 1000000 THEN '1-10 Lakhs'
				WHEN bp.total_sales >= 1000000 AND bp.total_sales < 2500000 THEN '10-25 Lakhs'
				WHEN bp.total_sales >= 2500000 AND bp.total_sales < 5000000 THEN '25-50 Lakhs'
				ELSE 'More than 50 Lakhs'
			END AS total_sales_range
		FROM
			`tabFPO` AS _fpo
		LEFT JOIN `tabBusiness Plannings` AS bp ON _fpo.name = bp.fpo
		LEFT JOIN `tabFinancial Year` AS _fy ON bp.financial_year = _fy.name
		LEFT JOIN `tabFPO Profiling` AS _fp ON bp.fpo = _fp.name_of_the_fpo
		WHERE 1 = 1 {financial_year_cond}{profitability_cond}{cond_str}{turnover_cond}
		"""
	# print(query,'='*100)
	columns = [
		{
			"fieldname": "fpo_name",
			"label": "FPO Name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "financial_year",
			"label": "Financial Year",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "turnover",
			"label": "Turnover",
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "total_sales_range",
			"label": "Total Sales Range",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "contact_detail_of_fpo",
			"label": "Contact Detail of FPO",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "fpo_email_id",
			"label": "FPO Email ID",
			"fieldtype": "Data",
			"width": 200
		}
	]
	data = frappe.db.sql(query, as_dict=True)
	return columns, data
