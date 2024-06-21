import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {
            "fieldname": "name",
            "label": _("Name"),
            "fieldtype": "Data",
            "width": 400
        },
        {
            "fieldname": "pending_count",
            "label": _("Pending"),
            "fieldtype": "Int",
            "width": 300
        },
        {
            "fieldname": "fund_was_received_before_due_date",
            "label": _("Fund was received before due date"),
            "fieldtype": "Int",
            "width": 300
        },
        {
            "fieldname": "fund_was_received_after_due_date",
            "label": _("Fund was received after due date"),
            "fieldtype": "Int",
            "width": 300
        }
    ]

    sql_query = """
        SELECT
            'Third Installment' AS name,
            SUM(CASE WHEN are_you_received_3rd_installment_fund = 'No' AND 3rd_installment_due_date < CURDATE() THEN 1 ELSE 0 END) AS pending_count,
            SUM(CASE WHEN are_you_received_3rd_installment_fund = 'Yes' AND 3rd_installment_date <= 3rd_installment_due_date THEN 1 ELSE 0 END) AS fund_was_received_before_due_date,
            SUM(CASE WHEN are_you_received_3rd_installment_fund = 'Yes' AND 3rd_installment_date > 3rd_installment_due_date THEN 1 ELSE 0 END) AS fund_was_received_after_due_date
        FROM
            `tabSFAC Installment`
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
