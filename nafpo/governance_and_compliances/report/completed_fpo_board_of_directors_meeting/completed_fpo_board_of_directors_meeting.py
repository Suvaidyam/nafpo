import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    # Define the columns for the report
    columns = [
        {
            "fieldname": "fpo_name",
            "label": "FPO Name",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "fpo_contact_number",
            "label": "FPO Contact Number",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "financial_year",
            "label": "Financial Year",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "total_meeting",
            "label": "Total Meetings",
            "fieldtype": "Int",
            "width": 200
        }
    ]

    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
    mappings={'CBBO': ('no_alias', 'cbbo'), 'IA': ('no_alias', 'ia')},
    selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    
    sql_query = f"""
        SELECT
            fpo_profiling.name_of_the_fpo_copy AS fpo_name,
            fpo_profiling.contact_detail_of_fpo AS fpo_contact_number,
            `tabBoard of Directors Meeting Forms`.financial_year AS financial_year,
            COUNT(*) AS total_meeting
        FROM
            `tabBoard of Directors Meeting Forms`
        INNER JOIN
            `tabFPO Profiling` AS fpo_profiling ON `tabBoard of Directors Meeting Forms`.fpo = fpo_profiling.name_of_the_fpo
        WHERE
            `tabBoard of Directors Meeting Forms`.status = 'Completed' {cond_str}
        GROUP BY
            fpo_name, fpo_contact_number, financial_year
        HAVING
            COUNT(*) >= 4
    """

    try:
        data = frappe.db.sql(sql_query, as_dict=True)
        return columns, data
    
    except Exception as e:
        frappe.log_error(f"Error in executing report: {e}")
        return columns, []
