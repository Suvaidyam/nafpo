# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    cond_str = ""
    if filters.get("Has_Trained_Bod") == "Yes":
        cond_str = "HAVING training_count > 0"
    elif filters.get("Has_Trained_Bod") == "No":
        cond_str = "HAVING training_count = 0"
    
    query = f""" 
    SELECT
        subquery.fpo_name,
        subquery.contact_detail_of_fpo,
        subquery.fpo_email_id,
        CASE WHEN subquery.training_count > 0 THEN 'Yes' ELSE 'No' END AS Has_Training_Bod
    FROM (
        SELECT
            f.fpo_name AS fpo_name,
            COUNT(b.parent) AS training_count,
            fp.contact_detail_of_fpo,
            fp.fpo_email_id
        FROM
            `tabFPO` f
        LEFT JOIN
            `tabCapacity` c ON f.name = c.fpo
        LEFT JOIN
            `tabBOD KYC Child` b ON c.name = b.parent
        LEFT JOIN
            `tabFPO Profiling` fp ON f.name = fp.name_of_the_fpo
        GROUP BY
            f.name, fp.contact_detail_of_fpo, fp.fpo_email_id
        {cond_str}
    ) AS subquery
    JOIN `tabFPO` f ON subquery.fpo_name = f.fpo_name;
    """
    
    columns = [
        {
            "fieldname": "fpo_name",
            "label": "FPO Name",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "contact_detail_of_fpo",
            "label": "Contact Detail of FPO",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "fpo_email_id",
            "label": "FPO Email ID",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "Has_Training_Bod",
            "label": "Has Trained BOD",
            "fieldtype": "Data",
            "width": 300
        }
    ]
    
    data = frappe.db.sql(query, as_dict=True)
    return columns, data
