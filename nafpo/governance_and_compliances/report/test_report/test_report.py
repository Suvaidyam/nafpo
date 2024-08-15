import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    # Define the columns for the report
    columns = [
        {
            "fieldname": "form_type",
            "label": "Form Type",
            "fieldtype": "Data",
            "width": 300
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
            'Form INC-20A – BUSINESS COMMENCEMENT- MCA' AS form_type,
            COUNT(CASE WHEN inc_20_status = 'Pending' THEN fpo END) AS pending,
            COUNT(CASE WHEN inc_20_status = 'Completed' AND inc_20_submitted_on <= inc_20_due_date THEN fpo END) AS completed_before_due_date,
            COUNT(CASE WHEN inc_20_status = 'Completed' AND inc_20_submitted_on > inc_20_due_date THEN fpo END) AS completed_after_due_date
        FROM
            `tabOne Time Organization Registration Forms`
        WHERE
            inc_20_status IS NOT NULL
            {cond_str}

        UNION ALL

        SELECT
            'Form INC-22 - Registered Office Address - MCA' AS form_type,
            COUNT(CASE WHEN inc_22_status = 'Pending' THEN fpo END) AS pending,
            COUNT(CASE WHEN inc_22_status = 'Completed' AND inc_22_submitted_on <= inc_22_due_date THEN fpo END) AS completed_before_due_date,
            COUNT(CASE WHEN inc_22_status = 'Completed' AND inc_22_submitted_on > inc_22_due_date THEN fpo END) AS completed_after_due_date
        FROM
            `tabOne Time Organization Registration Forms`
        WHERE
            inc_22_status IS NOT NULL
            {cond_str}
            
        UNION ALL
        
        SELECT
            'Form ADT-1 - Auditor Appointment for First year' AS form_type,
            COUNT(CASE WHEN adt_1_status = 'Pending' THEN 1 END) AS pending,
            COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on <= adt_1_due_date THEN 1 END) AS completed_before_due_date,
            COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on > adt_1_due_date THEN 1 END) AS completed_after_due_date
        FROM
            `tabOne Time Organization Registration Forms`
        WHERE
            1=1 {cond_str}
    """

    # Execute the SQL query and fetch data
    data = frappe.db.sql(sql_query, as_dict=True)

    # Return the columns and data to be rendered in the report
    return columns, data
