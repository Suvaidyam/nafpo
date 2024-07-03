import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    # Define the columns for the report
    columns = [
        {
            "fieldname": "name",
            "label": "Form Name",
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

    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
    mappings={'CBBO': ('sfac_inst', 'cbbo'), 'IA': ('sfac_inst', 'ia')},
    selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else "1=1"

    # SQL query to fetch the counts of different statuses
    sql_query = f"""
        SELECT
            'Form INC-22 - Registered office Address - MCA' AS name,
            COUNT(CASE WHEN inc_22_status = 'Pending' THEN 1 END) AS pending_count,
            COUNT(CASE WHEN inc_22_status = 'Completed' AND inc_22_submitted_on <= inc_22_due_date THEN 1 END) AS completed_before_due_date_count,
            COUNT(CASE WHEN inc_22_status = 'Completed' AND inc_22_submitted_on > inc_22_due_date THEN 1 END) AS completed_after_due_date_count
        FROM
            `tabOne Time Organization Registration Forms`
        # WHERE
        #     {cond_str}
    """

    # Execute the SQL query and fetch data
    data = frappe.db.sql(sql_query, as_dict=True)

    # Return the columns and data to be rendered in the report
    return columns, data
