import frappe

def execute(filters=None):
    columns = [
        {
            "fieldname": "name",
            "label": "Name",
            "fieldtype": "Data",
            "width": 400
        },
        {
            "fieldname": "pending_count",
            "label": "Pending",
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

    sql_query = """
        SELECT
            'Fifth Installment' AS name,
            SUM(CASE WHEN are_you_received_6th_installment_fund = 'No' AND 6th_installment_due_date < CURDATE() THEN 1 ELSE 0 END) AS pending_count,
            SUM(CASE WHEN are_you_received_6th_installment_fund = 'Yes' AND 6th_installment_date <= 6th_installment_due_date THEN 1 ELSE 0 END) AS fund_was_received_before_due_date,
            SUM(CASE WHEN are_you_received_6th_installment_fund = 'Yes' AND 6th_installment_date > 6th_installment_due_date THEN 1 ELSE 0 END) AS fund_was_received_after_due_date
        FROM
            `tabSFAC Installment`
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
