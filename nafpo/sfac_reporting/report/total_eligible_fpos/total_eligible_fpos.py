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
    ]

    cond_str = ""
    cond_str = (" AND " + ReportFilter.rport_filter_by_user_permissions(mappings = {'FPO': ('sfac_inst', 'fpo')},selected_filters=['FPO'])) if ReportFilter.rport_filter_by_user_permissions(mappings = {'FPO': ('sfac_inst', 'fpo')},selected_filters=['FPO']) is not None else ""
    
    sql_query = f"""
        WITH pending_dates AS (
            SELECT
                DISTINCT fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                fpo_profiling.contact_detail_of_fpo AS `FPO Contact Number`,
                sfac_inst.1st_installment_due_date AS `Due Date`,
                'First Installment' AS Installment
            FROM
                `tabFPO MFR 10K` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.1st_installment_due_date <= CURDATE()

            UNION ALL

            SELECT
                DISTINCT fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                fpo_profiling.contact_detail_of_fpo AS `FPO Contact Number`,
                sfac_inst.2nd_installment_due_date AS `Due Date`,
                'Second Installment' AS Installment
            FROM
                `tabFPO MFR 10K` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.2nd_installment_due_date <= CURDATE()

            UNION ALL

            SELECT
                DISTINCT fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                fpo_profiling.contact_detail_of_fpo AS `FPO Contact Number`,
                sfac_inst.3rd_installment_due_date AS `Due Date`,
                'Third Installment' AS Installment
            FROM
                `tabFPO MFR 10K` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.3rd_installment_due_date <= CURDATE()

            UNION ALL

            SELECT
                DISTINCT fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                fpo_profiling.contact_detail_of_fpo AS `FPO Contact Number`,
                sfac_inst.4th_installment_due_date AS `Due Date`,
                'Fourth Installment' AS Installment
            FROM
                `tabFPO MFR 10K` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.4th_installment_due_date <= CURDATE()

            UNION ALL

            SELECT
                DISTINCT fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                fpo_profiling.contact_detail_of_fpo AS `FPO Contact Number`,
                sfac_inst.5th_installment_due_date AS `Due Date`,
                'Fifth Installment' AS Installment
            FROM
                `tabFPO MFR 10K` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.5th_installment_due_date <= CURDATE()

            UNION ALL

            SELECT
                DISTINCT fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                fpo_profiling.contact_detail_of_fpo AS `FPO Contact Number`,
                sfac_inst.6th_installment_due_date AS `Due Date`,
                'Sixth Installment' AS Installment
            FROM
                `tabFPO MFR 10K` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.6th_installment_due_date <= CURDATE()
        )

        SELECT
            pd.`FPO Name` AS `fpo_name`,
            pd.`FPO Contact Number` AS `fpo_contact_number`,
            pd.Installment AS `installment`,
            pd.`Due Date` AS `due_date`
        FROM
            pending_dates pd
    """

    # Applying filters
    if filters.get("installment_"):
        sql_query += f" WHERE pd.Installment = '{filters['installment_']}'"

    # Fetch the data
    data = frappe.db.sql(sql_query, as_dict=True)

    # Return columns and data
    return columns, data
