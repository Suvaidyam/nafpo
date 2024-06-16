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
            'AGM - Once in a year fpo need to organize AGM and pass the Audit report and other agenda' AS name,
            COUNT(CASE WHEN agm_status = 'Pending' THEN 1 END) AS pending_count,
            COUNT(CASE WHEN agm_status = 'Completed' AND agm_submitted_on <= agm_due_date THEN 1 END) AS completed_before_due_date_count,
            COUNT(CASE WHEN agm_status = 'Completed' AND agm_submitted_on > agm_due_date THEN 1 END) AS completed_after_due_date_count
        FROM
            `tabAnnual Compliance Forms`
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
