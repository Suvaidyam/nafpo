import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    # Define columns
    columns = [
        {
            "fieldname": "fpo_name",
            "label": "FPO Name",
            "fieldtype": "Data",
            "width": 400
        },
        {
            "fieldname": "fpo_contact_number",
            "label": "FPO Contact Number",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "installment",
            "label": "Installment",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "due_date",
            "label": "Eligible Date",
            "fieldtype": "Date",
            "width": 300
        },
        {
            "fieldname": "total_fpo_count",
            "label": "Total Fpo Count",
            "fieldtype": "Int",
            "width": 300
        }
    ]
    cond_str = ReportFilter.rport_filter_by_user_permissions(table='sfac_inst')
    print('=================================cond_str', cond_str)

    # SQL Query to fetch the data
    sql_query = f"""
        WITH pending_dates AS (
            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.1st_installment_due_date AS `Due Date`,
                'First Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.1st_installment_due_date <= CURDATE() {cond_str}

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.2nd_installment_due_date AS `Due Date`,
                'Second Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.2nd_installment_due_date <= CURDATE() {cond_str}

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.3rd_installment_due_date AS `Due Date`,
                'Third Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.3rd_installment_due_date <= CURDATE() {cond_str}

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.4th_installment_due_date AS `Due Date`,
                'Fourth Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.4th_installment_due_date <= CURDATE() {cond_str}

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.5th_installment_due_date AS `Due Date`,
                'Fifth Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.5th_installment_due_date <= CURDATE() {cond_str}

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.6th_installment_due_date AS `Due Date`,
                'Sixth Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.6th_installment_due_date <= CURDATE() {cond_str}
        )

        SELECT
            pd.`FPO Name` AS `fpo_name`,
            fpo_profiling.contact_detail_of_fpo AS `fpo_contact_number`,
            pd.Installment AS `installment`,
            pd.`Due Date` AS `due_date`
        FROM
            pending_dates pd
        INNER JOIN
            `tabFPO Profiling` AS fpo_profiling ON pd.`FPO Name` = fpo_profiling.name_of_the_fpo_copy
    """

    # Applying filters
    if filters.get("installment_"):
        sql_query += f" WHERE pd.Installment = '{filters['installment_']}'"

    # Fetch the data
    data = frappe.db.sql(sql_query, as_dict=True)

    # Calculate total count
    total_count = len(data)
    print('=====================',total_count)
    

    # Append total count row
    data.append({
        'fpo_name': 'Total FPO Count',
        'fpo_contact_number': '',
        'installment': '',
        'due_date': '',
        'total_fpo_count': total_count
    })

    # Return columns and data
    return columns, data
