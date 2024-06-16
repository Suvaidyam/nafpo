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
            "fieldname": "completed_before_due_date_count",
            "label": "Completed Before Due Date",
            "fieldtype": "Int",
            "width": 300
        },
        {
            "fieldname": "completed_after_due_date_count",
            "label": "Completed After Due Date",
            "fieldtype": "Int",
            "width": 300
        }
    ]

    sql_query = """
        SELECT
            'DIRECTOR KYC' AS name,
            COUNT(CASE WHEN d_kyc_status = 'Pending' THEN 1 END) AS pending_count,
            COUNT(CASE WHEN d_kyc_status = 'Completed' AND d_kyc_submitted_on <= d_kyc_due_date THEN 1 END) AS completed_before_due_date_count,
            COUNT(CASE WHEN d_kyc_status = 'Completed' AND d_kyc_submitted_on > d_kyc_due_date THEN 1 END) AS completed_after_due_date_count
        FROM
            `tabAnnual Compliance Forms`
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
