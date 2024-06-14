# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

# import frappe

import frappe

def execute(filters=None):
    columns = [
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "count",
            "label": "Count",
            "fieldtype": "Int",
            "width": 300
        }
    ]
    
    sql_query = """
        SELECT 
            'INC-20A Pending Count' AS status,
            COUNT(CASE WHEN inc_20_status = 'Pending' THEN 1 END) AS count
        FROM 
            `tabOne Time Organization Registration Forms`
        UNION ALL
        SELECT 
            'INC-20A Completed Before Due Date' AS status,
            COUNT(CASE WHEN inc_20_status = 'Completed' AND inc_20_submitted_on <= inc_20_due_date THEN 1 END) AS count
        FROM 
            `tabOne Time Organization Registration Forms`
        UNION ALL
        SELECT 
            'INC-20A Completed After Due Date' AS status,
            COUNT(CASE WHEN inc_20_status = 'Completed' AND inc_20_submitted_on > inc_20_due_date THEN 1 END) AS count
        FROM 
            `tabOne Time Organization Registration Forms`
        UNION ALL
        SELECT 
            'INC-22 Pending Count' AS status,
            COUNT(CASE WHEN inc_22_status = 'Pending' THEN 1 END) AS count
        FROM 
            `tabOne Time Organization Registration Forms`
        UNION ALL
        SELECT 
            'INC-22 Completed Before Due Date' AS status,
            COUNT(CASE WHEN inc_22_status = 'Completed' AND inc_22_submitted_on <= inc_22_due_date THEN 1 END) AS count
        FROM 
            `tabOne Time Organization Registration Forms`
        UNION ALL
        SELECT 
            'INC-22 Completed After Due Date' AS status,
            COUNT(CASE WHEN inc_22_status = 'Completed' AND inc_22_submitted_on > inc_22_due_date THEN 1 END) AS count
        FROM 
            `tabOne Time Organization Registration Forms`
        UNION ALL
        SELECT 
            'ADT-1 Pending Count' AS status,
            COUNT(CASE WHEN adt_1_status = 'Pending' THEN 1 END) AS count
        FROM 
            `tabOne Time Organization Registration Forms`
        UNION ALL
        SELECT 
            'ADT-1 Completed Before Due Date' AS status,
            COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on <= adt_1_due_date THEN 1 END) AS count
        FROM 
            `tabOne Time Organization Registration Forms`
        UNION ALL
        SELECT 
            'ADT-1 Completed After Due Date' AS status,
            COUNT(CASE WHEN adt_1_status = 'Completed' AND adt_1_submitted_on > adt_1_due_date THEN 1 END) AS count
        FROM 
            `tabOne Time Organization Registration Forms`
    """
    
    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
