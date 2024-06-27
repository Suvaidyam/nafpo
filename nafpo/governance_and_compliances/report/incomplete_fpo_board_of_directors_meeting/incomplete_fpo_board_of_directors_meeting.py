import frappe

def execute(filters=None):
    # Define the columns for the report
    columns = [
        {
            "fieldname": "fpo",
            "label": "FPO",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "financial_year",
            "label": "Financial Year",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "total_meeting",
            "label": "Total Meeting",
            "fieldtype": "Int",
            "width": 200
        },
        {
            "fieldname": "total_fpo",
            "label": "Total FPOs",
            "fieldtype": "Int",
            "width": 200
        }
    ]

    # SQL query to fetch FPOs and their meeting counts
    sql_query = """
        SELECT
            fpo,
            financial_year,
            COUNT(*) AS total_meeting
        FROM
            `tabBoard of Directors Meeting Forms`
        WHERE
            status = 'Completed'
        GROUP BY
            fpo, financial_year
        HAVING
            COUNT(*) <= 3
        
    """

    # Execute the query to fetch the data
    data = frappe.db.sql(sql_query, as_dict=True)

    # SQL query to count the number of unique FPOs
    fpo_count_query = """
        SELECT
            COUNT(DISTINCT fpo) AS fpo_count
        FROM
            `tabBoard of Directors Meeting Forms`
        WHERE
            status = 'Completed' 
        GROUP BY
            fpo
        HAVING
            COUNT(*) <= 3
    """

    # Execute the query to count unique FPOs
    fpo_count_data = frappe.db.sql(fpo_count_query, as_dict=True)

    # Add a summary row for the count of unique FPOs
    fpo_count = len(fpo_count_data)
    print('============================ fpo_count_data',fpo_count)
    summary_row = {
        "fpo": "",
        "financial_year": "",
        "total_meeting": "",
        "total_fpo": fpo_count
    }
    data.append(summary_row)
    
    # Return the columns and data
    return columns, data
