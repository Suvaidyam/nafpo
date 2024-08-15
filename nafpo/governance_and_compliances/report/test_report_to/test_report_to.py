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
            'Form ADT-1 - Auditor Appointment for Five year' AS name,
            COUNT(DISTINCT CASE WHEN adt_1_status = 'Pending' THEN fpo END) AS pending,
            COUNT(DISTINCT CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on <= adt_1_due_date THEN fpo END) AS completed_before_due_date,
            COUNT(DISTINCT CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on > adt_1_due_date THEN fpo END) AS completed_after_due_date
        FROM
            `tabAnnual Compliance Forms`
        WHERE
            1=1 {cond_str}

        UNION ALL

        SELECT
            'AGM - Once in a year fpo need to organize AGM and pass the Audit report and other agenda' AS name,
            COUNT(DISTINCT CASE WHEN agm_status = 'Pending' THEN fpo END) AS pending,
            COUNT(DISTINCT CASE WHEN agm_status = 'Completed' AND agm_submitted_on <= agm_due_date THEN fpo END) AS completed_before_due_date,
            COUNT(DISTINCT CASE WHEN agm_status = 'Completed' AND agm_submitted_on > agm_due_date THEN fpo END) AS completed_after_due_date
        FROM
            `tabAnnual Compliance Forms`
        WHERE
            1=1 {cond_str}
        
        UNION ALL
        
        SELECT
            'IT Return' AS name,
            COUNT(DISTINCT CASE WHEN it_return_status = 'Pending' THEN fpo END) AS pending,
            COUNT(DISTINCT CASE WHEN it_return_status = 'Completed' AND it_return_submitted_on <= it_return_due_date THEN fpo END) AS completed_before_due_date,
            COUNT(DISTINCT CASE WHEN it_return_status = 'Completed' AND it_return_submitted_on > it_return_due_date THEN fpo END) AS completed_after_due_date
        FROM
            `tabAnnual Compliance Forms`
        WHERE
            1=1 {cond_str}
            
        UNION ALL
        
        SELECT
            'FORM AOC-4 – Filing of Financial Statements' AS name,
            COUNT(CASE WHEN aoc_4_status = 'Pending' THEN fpo END) AS pending,
            COUNT(CASE WHEN aoc_4_status = 'Completed' AND aoc_4_submitted_on <= aoc_4_due_date THEN fpo END) AS completed_before_due_date,
            COUNT(CASE WHEN aoc_4_status = 'Completed' AND aoc_4_submitted_on > aoc_4_due_date THEN fpo END) AS completed_after_due_date
        FROM
            `tabAnnual Compliance Forms`
        WHERE
            1=1 {cond_str}
            
        UNION ALL
        
        SELECT
            'Form MGT-7 - Filing of Annual Return' AS name,
            COUNT(CASE WHEN mgt_7_status = 'Pending' THEN 1 END) AS pending,
            COUNT(CASE WHEN mgt_7_status = 'Completed' AND mgt_7_submitted_on <= mgt_7_due_date THEN 1 END) AS completed_before_due_date,
            COUNT(CASE WHEN mgt_7_status = 'Completed' AND mgt_7_submitted_on > mgt_7_due_date THEN 1 END) AS completed_after_due_date
        FROM
            `tabAnnual Compliance Forms`
        WHERE
            1=1 {cond_str}
            
		UNION ALL

        SELECT
            'DIRECTOR KYC' AS name,
            COUNT(CASE WHEN d_kyc_status = 'Pending' THEN 1 END) AS pending,
            COUNT(CASE WHEN d_kyc_status = 'Completed' AND d_kyc_submitted_on <= d_kyc_due_date THEN 1 END) AS completed_before_due_date,
            COUNT(CASE WHEN d_kyc_status = 'Completed' AND d_kyc_submitted_on > d_kyc_due_date THEN 1 END) AS completed_after_due_date
        FROM
            `tabAnnual Compliance Forms`
        WHERE
            1=1 {cond_str}
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
