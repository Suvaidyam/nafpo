import frappe
class ReportFilter:
    def rport_filter_by_user_permissions(table=None,ia_key='ia',cbbo_key='cbbo'):
        permissions = frappe.db.get_list("User Permission",filters={'user':frappe.session.user},fields=['allow','for_value'],ignore_permissions=True)
        perm_arr = []
        final_cond = None
        if(len(permissions)):
            perm_dict = {perm['allow']: perm['for_value'] for perm in permissions}
            ia = perm_dict.get('IA') or None
            cbbo = perm_dict.get('CBBO') or None
            perm_str = ''
            if ia is not None:
                perm_str = f"{ia_key if table is None else f'{table}.{ia_key}'} = '{ia}'"
            if cbbo is not None:
                perm_str = f"{cbbo_key if table is None else f'{table}.{cbbo_key}'} = '{cbbo}'"
            perm_arr.append(perm_str)
            final_cond = " AND ".join(perm_arr)
        return f"AND {final_cond}" if final_cond is not None else ""