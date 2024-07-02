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
    mappings={'CBBO': ('sfac_inst', 'cbbo'), 'IA': ('sfac_inst', 'ia')},
    selected_filters=['CBBO', 'IA']
    )
    cond_str = f"{user_filter_conditions}" if user_filter_conditions else "1=1"

    sql_query = f"""
        SELECT
            'Fifth Installment' AS name,
            SUM(CASE WHEN are_you_received_6th_installment_fund = 'No' AND 6th_installment_due_date < CURDATE() THEN 1 ELSE 0 END) AS eligible_fpo,
            SUM(CASE WHEN are_you_received_6th_installment_fund = 'Yes' AND 6th_installment_date <= 6th_installment_due_date THEN 1 ELSE 0 END) AS fund_was_received_before_due_date,
            SUM(CASE WHEN are_you_received_6th_installment_fund = 'Yes' AND 6th_installment_date > 6th_installment_due_date THEN 1 ELSE 0 END) AS fund_was_received_after_due_date
        FROM
            `tabFPO MFR 10K`
        WHERE
            {cond_str}
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
