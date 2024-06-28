import frappe

def execute(filters=None):
    # Define columns for the report
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
            "fieldname": "due_date",
            "label": "Due Date",
            "fieldtype": "Date",
            "width": 300
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Data",
            "width": 300
        }
    ]

    # Initialize conditions list
    conditions = []

    # Construct conditions based on filters
    if filters:
        if filters.get("status") == "Pending":
            conditions.append("otorf.adt_1_status = 'Pending'")
        elif filters.get("status") == "Completed Before Due Date":
            conditions.append("otorf.adt_1_status = 'Completed' AND otorf.adt_1_submitted_on <= otorf.adt_1_due_date")
        elif filters.get("status") == "Completed After Due Date":
            conditions.append("otorf.adt_1_status = 'Completed' AND otorf.adt_1_submitted_on > otorf.adt_1_due_date")

    # Construct WHERE clause if conditions exist
    if conditions:
        sql_query = f"""
            SELECT
                fpo_profiling.name_of_the_fpo_copy AS fpo_name,
                fpo_profiling.contact_detail_of_fpo AS fpo_contact_number,
                otorf.adt_1_due_date AS due_date,
                otorf.adt_1_status AS status
            FROM
                `tabOne Time Organization Registration Forms` AS otorf
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON otorf.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                {' AND '.join(conditions)}
            GROUP BY
                fpo_profiling.name_of_the_fpo_copy
        """
    else:
        # If no filters provided, retrieve all records
        sql_query = """
            SELECT
                fpo_profiling.name_of_the_fpo_copy AS fpo_name,
                fpo_profiling.contact_detail_of_fpo AS fpo_contact_number,
                otorf.adt_1_due_date AS due_date,
                otorf.adt_1_status AS status
            FROM
                `tabOne Time Organization Registration Forms` AS otorf
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON otorf.fpo = fpo_profiling.name_of_the_fpo
            GROUP BY
                fpo_profiling.name_of_the_fpo_copy
        """

    # Execute the SQL query and fetch data
    data = frappe.db.sql(sql_query, as_dict=True)

    # Return columns and data for rendering in the report
    return columns, data
