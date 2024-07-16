import frappe
from nafpo.utils.rport_filter import ReportFilter
import datetime

@frappe.whitelist()
def fpo_with_current_year_business_planning():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('_fpo', 'cbbo_name'),'IA': ('_fpo', 'ia'),'FPO': ('_fpo', 'name')},
        selected_filters=['FPO','CBBO','IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    financial_year_cond = ''
    current_year = datetime.datetime.now().year
    financial_year = frappe.get_list('Financial Year', filters={'start_date': ['between', [f'{current_year}-01-01', f'{current_year}-12-31']]},pluck='name')[0] or None
    if financial_year is not None:
        financial_year_cond = f" AND bp.financial_year = '{financial_year}'"
    query = f"""
        SELECT
            COUNT(DISTINCT bp.fpo) AS count
        FROM
            `tabBusiness Plannings` AS bp
        INNER JOIN `tabFPO` AS _fpo ON bp.fpo = _fpo.name
        WHERE
            1=1 {financial_year_cond}{cond_str}
    """
    count= frappe.db.sql(query, as_dict=1)
    return count[0]