import frappe
from frappe.model.document import Document

class OneTimeOrganizationRegistrationForms(Document):
    def before_validate(self):
        exists = frappe.db.exists({
            "doctype": "One Time Organization Registration Forms", 
            "fpo": self.fpo
        })
        data_exists = bool(exists)
        if data_exists and exists != self.name:
            frappe.throw(f"FPO already exists in One Time Organization Registration Forms")
        
        check_exist_profile = frappe.db.exists({
            "doctype": "FPO Profiling", 
            "name_of_the_fpo": self.fpo
        })
        if check_exist_profile == None:
            frappe.throw(f"FPO Profile doesn't exist. Please create FPO Profiling.")