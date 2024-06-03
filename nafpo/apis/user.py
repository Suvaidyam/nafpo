import frappe

@frappe.whitelist(allow_guest=True)
def get_user_permission(user, join_con=[]):
    # sql_query = f""" SELECT allow,for_value FROM `tabUser Permission` WHERE user = '{user}' """
    sql_query = f"""
        SELECT
            CASE
                WHEN UP.allow = 'IA' THEN IA.name1
                WHEN UP.allow = 'CBBO' THEN CBBO.name_of_cbbo
                WHEN UP.allow = 'FPO' THEN FPO.fpo_name
            END AS name_value,
            UP.for_value,
            UP.name,
            UP.allow,
            UP.user
        FROM `tabUser Permission` AS UP
        LEFT JOIN `tabIA` AS IA ON UP.for_value = IA.name AND UP.allow = 'IA'
        LEFT JOIN `tabCBBO` AS CBBO ON UP.for_value = CBBO.name AND UP.allow = 'CBBO'
        LEFT JOIN `tabFPO` AS FPO ON UP.for_value = FPO.name AND UP.allow = 'FPO'
        WHERE UP.user = '{user}'
    """
    return frappe.db.sql(sql_query, as_dict=True)