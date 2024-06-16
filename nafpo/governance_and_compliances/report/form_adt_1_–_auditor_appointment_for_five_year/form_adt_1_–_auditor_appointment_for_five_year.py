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
            'Form ADT-1 - Auditor Appointment for Five year' AS name,
            COUNT(CASE WHEN adt_1_status = 'Pending' THEN 1 END) AS pending_count,
            COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on <= adt_1_due_date THEN 1 END) AS completed_before_due_date_count,
            COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on > adt_1_due_date THEN 1 END) AS completed_after_due_date_count
        FROM
            `tabAnnual Compliance Forms`
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
