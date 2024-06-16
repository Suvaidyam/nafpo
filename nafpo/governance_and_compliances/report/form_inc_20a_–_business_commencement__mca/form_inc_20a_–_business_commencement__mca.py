import frappe

def execute(filters=None):
    # Define the columns for the report
    columns = [
        {
            "fieldname": "name",
            "label": "Name",
            "fieldtype": "Data",
            "width": 300
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
            'Form INC-20A – BUSINESS COMMENCEMENT- MCA' AS name,
            COUNT(CASE WHEN inc_20_status = 'Pending' THEN 1 END) AS pending_count,
            COUNT(CASE WHEN inc_20_status = 'Completed' AND inc_20_submitted_on <= inc_20_due_date THEN 1 END) AS completed_before_due_date_count,
            COUNT(CASE WHEN inc_20_status = 'Completed' AND inc_20_submitted_on > inc_20_due_date THEN 1 END) AS completed_after_due_date_count
        FROM
            `tabOne Time Organization Registration Forms`
        # UNION ALL
        # SELECT
        #     'INC-22' AS status,
        #     COUNT(CASE WHEN inc_22_status = 'Pending' THEN 1 END) AS pending_count,
        #     COUNT(CASE WHEN inc_22_status = 'Completed' AND inc_22_submitted_on <= inc_22_due_date THEN 1 END) AS completed_before_due_date_count,
        #     COUNT(CASE WHEN inc_22_status = 'Completed' AND inc_22_submitted_on > inc_22_due_date THEN 1 END) AS completed_after_due_date_count
        # FROM
        #     `tabOne Time Organization Registration Forms`
        # UNION ALL
        # SELECT
        #     'ADT-1' AS status,
        #     COUNT(CASE WHEN adt_1_status = 'Pending' THEN 1 END) AS pending_count,
        #     COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on <= adt_1_due_date THEN 1 END) AS completed_before_due_date_count,
        #     COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on > adt_1_due_date THEN 1 END) AS completed_after_due_date_count
        # FROM
        #     `tabOne Time Organization Registration Forms`
    """

    # Execute the SQL query and fetch data
    data = frappe.db.sql(sql_query, as_dict=True)

    # Return the columns and data to be rendered in the report
    return columns, data
