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
            "fieldname": "completed",
            "label": "Completed",
            "fieldtype": "Int",
            "width": 300
        },
    ]

    sql_query = """
        SELECT
            'Board of Directors Meeting Forms' AS name,
            COUNT(CASE WHEN status != 'Completed' THEN 1 END) AS pending_count,
            CASE 
                WHEN COUNT(CASE WHEN status = 'Completed' THEN 1 END) >= 4 
                THEN 'Completed' 
                ELSE 'Not Completed' 
            END AS completed
        FROM
            `tabBoard of Directors Meeting Forms`
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
