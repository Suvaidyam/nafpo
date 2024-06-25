import frappe

@frappe.whitelist()
def get_fpo_profile(name=None, fields=["*"]):
    parent = frappe.db.exists({'doctype':'FPO Profiling','name_of_the_fpo':name})
    child_filter = {'parent': parent,'parenttype': 'FPO Profiling','parentfield': 'bod_kyc_name'}
    print('============== child_filter',child_filter)
    data = frappe.get_list('BOD KYC Child',
        filters=child_filter,
        fields=fields,
        page_length=10000,
        ignore_permissions = True
    )
    final_fpo_data = []
    for d in data:
        name = frappe.db.get_value('BOD KYC',d.bod_kyc,'name1')
        final_fpo_data.append(name)
    return final_fpo_data

@frappe.whitelist()
def get_fpo_profile_doc(doctype_name,filter):
    return frappe.db.get_value(doctype_name, {'name_of_the_fpo':filter },['date_of_registration'],as_dict=1)

