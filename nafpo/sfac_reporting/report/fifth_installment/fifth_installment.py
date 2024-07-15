import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    columns = [
        {
            "fieldname": "name",
            "label": "Name",
            "fieldtype": "Data",
            "width": 400
        },
        {
            "fieldname": "eligible_fpo",
            "label": "Eligible FPO",
            "fieldtype": "Int",
            "width": 300
        },
        {
            "fieldname": "eligible_but_have_received_fund_yet",
            "label": "Eligible but haven't received fund yet",
            "fieldtype": "Int",
            "width": 300
        },
        {
            "fieldname": "fund_was_received_before_due_date",
            "label": "Fund was received before due date",
            "fieldtype": "Int",
            "width": 300
        },
        {
            "fieldname": "fund_was_received_after_due_date",
            "label": "Fund was received after due date",
            "fieldtype": "Int",
            "width": 300
        }
    ]

    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('no_alias', 'cbbo'), 'IA': ('no_alias', 'ia')},
        selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""

    sql_query = f"""
        SELECT
            'Fifth Installment' AS name,
            COUNT(DISTINCT CASE WHEN 5th_installment_due_date <= CURDATE() THEN fpo END) AS eligible_fpo,
            COUNT(DISTINCT CASE WHEN are_you_received_5th_installment_fund = 'Yes' AND 5th_installment_due_date <= CURDATE() THEN fpo END) AS eligible_but_have_received_fund_yet,
            COUNT(DISTINCT CASE WHEN are_you_received_5th_installment_fund = 'Yes' AND 5th_installment_due_date >= 5th_installment_date THEN fpo END) AS fund_was_received_before_due_date,
            COUNT(DISTINCT CASE WHEN are_you_received_5th_installment_fund = 'Yes' AND 5th_installment_due_date < 5th_installment_date THEN fpo END) AS fund_was_received_after_due_date
        FROM
            `tabFPO MFR 10K`
        WHERE
            1=1 {cond_str}
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
