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
            "fieldname": "pending",
            "label": "Pending",
            "fieldtype": "Int",
            "width": 300
        },
        {
            "fieldname": "completed_before_due_date",
            "label": "Completed Before Due Date",
            "fieldtype": "Int",
            "width": 300
        },
        {
            "fieldname": "completed_after_due_date",
            "label": "Completed After Due Date",
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
            'Form ADT-1 - Auditor Appointment for First year' AS name,
            COUNT(CASE WHEN adt_1_status = 'Pending' THEN 1 END) AS pending,
            COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on <= adt_1_due_date THEN 1 END) AS completed_before_due_date,
            COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on > adt_1_due_date THEN 1 END) AS completed_after_due_date
        FROM
            `tabOne Time Organization Registration Forms`
        WHERE
            1=1 {cond_str}
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
