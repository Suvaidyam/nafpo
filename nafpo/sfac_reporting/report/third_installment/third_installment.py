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
            'Third Installment' AS name,
            COUNT(CASE WHEN are_you_received_3rd_installment_fund = 'No' THEN 1 END) AS pending_count,
            COUNT(CASE WHEN are_you_received_3rd_installment_fund = 'Yes' AND 3rd_installment_date <= 3rd_installment_due_date THEN 1 END) AS fund_was_received_before_due_date,
            COUNT(CASE WHEN are_you_received_3rd_installment_fund = 'Yes' AND 3rd_installment_date > 3rd_installment_due_date THEN 1 END) AS fund_was_received_after_due_date
        FROM
            `tabSFAC Installment`
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
