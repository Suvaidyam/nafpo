# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt
import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('f', 'cbbo_name'), 'State': ('f', 'state'), 'District': ('f', 'district'), 'FPO': ('f', 'name'), 'IA': ('p', 'ia')},
        selected_filters=['CBBO','State','FPO','District','IA']
    )
    user_cond_str = f"WHERE {user_filter_conditions}" if user_filter_conditions else ""
    
    cond_str = ""
    if filters.get("FPO_with_Training") == "Yes":
        cond_str = "HAVING COUNT(DISTINCT CASE WHEN c.fpo IS NOT NULL THEN f.name END) > 0"
    elif filters.get("FPO_with_Training") == "No":
        cond_str = "HAVING COUNT(DISTINCT CASE WHEN c.fpo IS NOT NULL THEN f.name END) = 0"
        
    query = f""" 
    SELECT
        f.fpo_name AS FPO_Name,
        CASE 
            WHEN COUNT(DISTINCT CASE WHEN c.fpo IS NOT NULL THEN f.name END) > 0 THEN 'Yes'
            ELSE 'No'
        END AS FPO_with_Training,
        p.fpo_email_id AS FPO_email_id,
        p.contact_detail_of_fpo AS FPO_Contact_Detail
    FROM `tabFPO` f
    LEFT JOIN `tabCapacity` c ON f.name = c.fpo
    LEFT JOIN `tabFPO Profiling` p ON f.name = p.name_of_the_fpo
    {user_cond_str}
    GROUP BY f.fpo_name, p.fpo_email_id, p.contact_detail_of_fpo
    {cond_str};
    """
    
    columns = [
        {
            "label": "FPO Name",
            "fieldname": "FPO_Name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "FPO with Training",
            "fieldname": "FPO_with_Training",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "FPO Email ID",
            "fieldname": "FPO_email_id",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "FPO Contact Detail",
            "fieldname": "FPO_Contact_Detail",
            "fieldtype": "Data",
            "width": 200
        }
    ]
    
    data = frappe.db.sql(query, as_dict=True)
    return columns, data
