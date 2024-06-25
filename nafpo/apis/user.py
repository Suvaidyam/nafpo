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
                WHEN UP.allow = 'State' THEN TS.state_name
                WHEN UP.allow = 'District' THEN TD.district_name
                WHEN UP.allow = 'Block' THEN TB.block_name
            END AS name_value,
            UP.for_value,
            UP.name,
            UP.allow,
            UP.user
        FROM `tabUser Permission` AS UP
        LEFT JOIN `tabIA` AS IA ON UP.for_value = IA.name AND UP.allow = 'IA'
        LEFT JOIN `tabCBBO` AS CBBO ON UP.for_value = CBBO.name AND UP.allow = 'CBBO'
        LEFT JOIN `tabFPO` AS FPO ON UP.for_value = FPO.name AND UP.allow = 'FPO'
        LEFT JOIN `tabState` AS TS ON UP.for_value = TS.name AND UP.allow = 'State'
        LEFT JOIN `tabDistrict` AS TD ON UP.for_value = TD.name AND UP.allow = 'District'
        LEFT JOIN `tabBlock` AS TB ON UP.for_value = TB.name AND UP.allow = 'Block'
        WHERE UP.user = '{user}'
    """
    return frappe.db.sql(sql_query, as_dict=True)