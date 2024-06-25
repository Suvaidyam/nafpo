import frappe

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
            "fieldname": "installment_date",
            "label": "Received Installment",
            "fieldtype": "Date",
            "width": 300
        },
        {
            "fieldname": "due_date",
            "label": "Eligible Date",
            "fieldtype": "Date",
            "width": 300
        }
    ]

    # SQL Query to fetch the data
    sql_query = """
        WITH pending_dates AS (
            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.1st_installment_due_date AS `Due Date`,
                sfac_inst.1st_installment_date AS `Installment Date`,
                'First Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.are_you_received_1st_installment_fund = 'Yes'
                AND sfac_inst.1st_installment_due_date >= CURDATE()

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.2nd_installment_due_date AS `Due Date`,
                sfac_inst.2nd_installment_date AS `Installment Date`,
                'Second Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.are_you_received_2nd_installment_fund = 'Yes'
                AND sfac_inst.2nd_installment_due_date >= CURDATE()

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.3rd_installment_due_date AS `Due Date`,
                sfac_inst.3rd_installment_date AS `Installment Date`,
                'Third Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.are_you_received_3rd_installment_fund = 'Yes'
                AND sfac_inst.3rd_installment_due_date >= CURDATE()

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.4th_installment_due_date AS `Due Date`,
                sfac_inst.4th_installment_date AS `Installment Date`,
                'Fourth Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.are_you_received_4th_installment_fund = 'Yes'
                AND sfac_inst.4th_installment_due_date >= CURDATE()

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.5th_installment_due_date AS `Due Date`,
                sfac_inst.5th_installment_date AS `Installment Date`,
                'Fifth Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.are_you_received_5th_installment_fund = 'Yes'
                AND sfac_inst.5th_installment_due_date >= CURDATE()

            UNION ALL

            SELECT
                fpo_profiling.name_of_the_fpo_copy AS `FPO Name`,
                sfac_inst.6th_installment_due_date AS `Due Date`,
                sfac_inst.6th_installment_date AS `Installment Date`,
                'Sixth Installment' AS Installment
            FROM
                `tabSFAC Installment` AS sfac_inst
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON sfac_inst.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                sfac_inst.are_you_received_6th_installment_fund = 'Yes'
                AND sfac_inst.6th_installment_due_date >= CURDATE()
        )

        SELECT
            pd.`FPO Name` AS `fpo_name`,
            fpo_profiling.contact_detail_of_fpo AS `fpo_contact_number`,
            pd.Installment AS `installment`,
            pd.`Installment Date` AS `installment_date`,
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

    # Return columns and data
    return columns, data
